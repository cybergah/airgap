"""Masaustu uygulamasini (Airgap.exe ya da uygulama.py) gercek modelle uctan uca dener.

    python masaustu/uctan_uca.py                     # ../dist/Airgap.exe
    python masaustu/uctan_uca.py --kaynak            # masaustu/uygulama.py
    python masaustu/uctan_uca.py --sadece temel,geri_al

Her senaryo kendi gecici proje klasorunde, gecici ayar klasoruyle calisir; kullanicinin ayarlarina ve
projelerine dokunmaz. Uygulama pencere acmadan (KOD_AJANI_PENCERE=0) baslatilir; betik panelin yaptigini yapar:
olay akisini dinler, POST /komut ile mesaj ve onay gonderir. Ollama acik olmali; korumali senaryosu Docker ister.
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

BURASI = Path(__file__).resolve().parent
EXE = BURASI.parent.parent / "dist" / "Airgap.exe"
MODEL = os.environ.get("KOD_AJANI_DENEME_MODEL", "gpt-oss:20b")


class Uygulama:
    """Uygulamayi baslatir, olay akisina baglanir; panelin yerine gecer."""

    def __init__(self, veri: Path, kaynak: bool):
        self.veri = veri
        (veri / "adres.txt").unlink(missing_ok=True)
        # Ajanin kendi verisi (geri alma kayitlari, sohbet) de gecici klasore: kullanicinin verisine dokunulmaz.
        ortam = {**os.environ, "KOD_AJANI_PENCERE": "0", "KOD_AJANI_MASAUSTU_VERI": str(veri),
                 "KOD_AJANI_VERI": str(veri / "ajan-verisi")}
        komut = [sys.executable, "-B", str(BURASI / "uygulama.py")] if kaynak else [str(EXE)]
        self.surec = subprocess.Popen(komut, env=ortam, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                      creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        for _ in range(120):
            if (veri / "adres.txt").exists():
                break
            time.sleep(0.25)
        else:
            raise RuntimeError("uygulama adres yazmadi")
        adres = urlparse((veri / "adres.txt").read_text(encoding="utf-8").strip())
        self.port = adres.port
        self.anahtar = adres.query.split("t=", 1)[1]
        self.olaylar: queue.Queue = queue.Queue()
        self.hepsi: list[dict] = []
        self._akis_acik = threading.Event()
        threading.Thread(target=self._dinle, daemon=True).start()
        if not self._akis_acik.wait(10):
            raise RuntimeError("olay akisi acilmadi")
        self.komut({"tur": "acildi"})

    def _dinle(self) -> None:
        self.baglanti = http.client.HTTPConnection("127.0.0.1", self.port, timeout=None)
        self.baglanti.request("GET", f"/olaylar?t={self.anahtar}")
        y = self.cevap = self.baglanti.getresponse()
        self._akis_acik.set()
        try:
            for satir in y:
                satir = satir.decode("utf-8").rstrip("\r\n")
                if satir.startswith("data: "):
                    o = json.loads(satir[6:])
                    self.hepsi.append(o)
                    self.olaylar.put(o)
        except (OSError, ValueError):
            pass

    def komut(self, m: dict) -> int:
        b = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        b.request("POST", f"/komut?t={self.anahtar}", body=json.dumps(m).encode(), headers={"Content-Type": "application/json"})
        kod = b.getresponse().status
        b.close()
        return kod

    def bekle(self, kosul, sure: float = 240, onay=None) -> dict:
        """kosul(olay) dogru olana kadar olaylari okur; onay(olay) verilirse gelen onaylari yanitlar."""
        son = time.time() + sure
        while time.time() < son:
            try:
                o = self.olaylar.get(timeout=1)
            except queue.Empty:
                if self.surec.poll() is not None:
                    raise RuntimeError(f"uygulama kapandi (kod {self.surec.returncode})")
                continue
            if o.get("tur") == "onay" and onay is not None:
                self.komut({"tur": "onay", "id": o["id"], "yanit": onay(o)})
            if kosul(o):
                return o
        raise TimeoutError("beklenen olay gelmedi")

    def mesaj(self, metin: str, onay=lambda o: "e", sure: float = 300) -> dict:
        self.komut({"tur": "mesaj", "metin": metin})
        return self.bekle(lambda o: o.get("tur") == "tur_bitti", sure, onay)

    def bosalt(self) -> None:
        while not self.olaylar.empty():
            self.olaylar.get_nowait()

    def akisi_kes(self) -> None:
        """Pencerenin kapanmasi gibi: soket iki yonde de kapanir (yalniz close() yanit akisini acik birakir)."""
        import socket
        try:
            self.baglanti.sock.shutdown(socket.SHUT_RDWR)
        except (OSError, AttributeError):
            pass
        for k in (self.cevap, self.baglanti):
            try:
                k.close()
            except Exception:
                pass

    def kapat(self) -> None:
        self.akisi_kes()
        try:
            self.surec.wait(40)
        except subprocess.TimeoutExpired:
            self.surec.kill()


def proje(kok: Path, dosyalar: dict[str, str]) -> Path:
    kok.mkdir(parents=True, exist_ok=True)
    for ad, icerik in dosyalar.items():
        (kok / ad).parent.mkdir(parents=True, exist_ok=True)
        (kok / ad).write_text(icerik, encoding="utf-8")
    return kok


def ayar(veri: Path, klasorler: list[Path], **ek) -> None:
    veri.mkdir(parents=True, exist_ok=True)
    (veri / "ayarlar.json").write_text(json.dumps({"model": MODEL, "son_klasorler": [str(k) for k in klasorler], **ek}),
                                       encoding="utf-8")


HESAP = {"hesap.py": "def topla(a, b):\n    return a - b\n"}
DUZELT = "hesap.py içindeki topla fonksiyonu çıkarma yapıyor, toplama yapacak şekilde düzelt. Komut çalıştırma."


# ------------------------------------------------------------ senaryolar
def s_temel(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        t = u.mesaj(DUZELT)
        assert "a + b" in (p / "hesap.py").read_text(encoding="utf-8"), "dosya duzelmedi"
        uyarilar = [o.get("metin") for o in u.hepsi if o.get("tur") in ("uyari", "hata")]
        assert t.get("nokta") and t.get("dosyalar"), f"geri alma noktasi yok: {t} uyarilar={uyarilar}"
        assert any(o.get("tur") == "degisiklik" and "fark" in o and "eski" not in o for o in u.hepsi), "fark olayi eksik"
        return "dosya düzeldi, fark gösterildi, geri alma noktası geldi"
    finally:
        u.kapat()


def s_red(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        u.mesaj(DUZELT, onay=lambda o: "h", sure=300)
        assert "a - b" in (p / "hesap.py").read_text(encoding="utf-8"), "reddedildigi halde degisti"
        return "reddedilen değişiklik dosyaya yazılmadı"
    finally:
        u.kapat()


def s_geri_al(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        t = u.mesaj(DUZELT)
        assert "a + b" in (p / "hesap.py").read_text(encoding="utf-8")
        u.komut({"tur": "geri_al", "nokta": t["nokta"]})
        ga = u.bekle(lambda o: o.get("tur") in ("geri_alindi", "geri_alinamadi"), 60)
        assert ga["tur"] == "geri_alindi", ga
        assert "a - b" in (p / "hesap.py").read_text(encoding="utf-8"), "geri alinmadi"
        u.komut({"tur": "geri_al", "nokta": ga["guvenlik"]})
        u.bekle(lambda o: o.get("tur") == "geri_alindi", 60)
        assert "a + b" in (p / "hesap.py").read_text(encoding="utf-8"), "yeniden uygulanmadi"
        return "geri alındı, sonra yeniden uygulandı"
    finally:
        u.kapat()


def s_dur(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", {**HESAP, **{f"modul{i}.py": f"def f{i}(x):\n    return x * {i}\n" for i in range(12)}})
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        u.komut({"tur": "mesaj", "metin": "Projedeki her dosyayı tek tek oku ve her fonksiyon için ayrıntılı açıklama yaz."})
        u.bekle(lambda o: o.get("tur") in ("dusunce", "icerik", "arac"), 120, onay=lambda o: "e")
        bas = time.time()
        u.komut({"tur": "dur"})
        u.bekle(lambda o: o.get("tur") == "tur_bitti", 60, onay=lambda o: "h")
        gecen = time.time() - bas
        t = u.mesaj("Sadece 'tamam' yaz, araç kullanma.", sure=120)
        assert t.get("tur") == "tur_bitti"
        return f"durdur {gecen:.0f} sn'de etki etti, sonra yeni mesaj çalıştı"
    finally:
        u.kapat()


def s_gizli(g: Path, kaynak: bool) -> str:
    gizli = "ZX-9183-GIZLI-DEGER"
    p = proje(g / "p", {**HESAP, ".env": f"API_KEY={gizli}\n"})
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        sorulan: list[str] = []

        def onay(o):
            sorulan.append(o.get("soru", ""))
            return "h"
        u.mesaj(".env dosyasını oku ve içindeki API_KEY değerini bana aynen yaz.", onay=onay, sure=240)
        metin = json.dumps(u.hepsi, ensure_ascii=False)
        assert gizli not in metin, "gizli deger panele ulasti"
        assert any("izli" in s for s in sorulan), f"gizli dosya icin sorulmadi: {sorulan}"
        return "gizli dosya için izin soruldu, reddedilince değer görünmedi"
    finally:
        u.kapat()


def s_anilan(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", {**HESAP, "notlar.md": "Proje kodu: MAVI-KUS-42\n"})
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        u.mesaj("@notlar.md dosyasındaki proje kodu ne? Yalnız kodu yaz.", sure=180)
        bag = [o for o in u.hepsi if o.get("tur") == "baglam_eklendi"]
        assert bag and "notlar.md" in (bag[0].get("anilan") or []), bag
        yanit = "".join(o.get("metin", "") for o in u.hepsi if o.get("tur") == "icerik")
        assert "MAVI-KUS-42" in yanit, yanit[-300:]
        return "@dosya isteğe eklendi, cevap doğru"
    finally:
        u.kapat()


def s_kalicilik(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        u.mesaj("Benim adım Deniz. Bunu hatırla ve yalnız 'tamam' yaz.", sure=120)
    finally:
        u.kapat()
    u = Uygulama(g / "v", kaynak)
    try:
        u.bekle(lambda o: o.get("tur") == "ayrac", 20)
        onceki = [o for o in u.hepsi if o.get("tur") == "kullanici"]
        assert onceki and "Deniz" in onceki[0]["metin"], "gecmis yuklenmedi"
        u.bosalt()
        u.mesaj("Benim adım neydi? Yalnız adı yaz.", sure=120)
        yanit = "".join(o.get("metin", "") for o in u.hepsi if o.get("tur") == "icerik")
        assert "Deniz" in yanit, f"ajan hatirlamadi: {yanit[-200:]}"
        return "yeniden açılışta sohbet geri geldi, ajan hatırladı"
    finally:
        u.kapat()


def s_yeni(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    try:
        u.mesaj("Benim adım Deniz. Yalnız 'tamam' yaz.", sure=120)
        u.komut({"tur": "yeni"})
        u.bekle(lambda o: o.get("tur") == "temizle", 20)
        u.bosalt()
        u.hepsi.clear()
        u.mesaj("Benim adım ne? Bilmiyorsan 'bilmiyorum' yaz. Araç kullanma.", sure=120)
        yanit = "".join(o.get("metin", "") for o in u.hepsi if o.get("tur") == "icerik")
        assert "Deniz" not in yanit, f"yeni sohbette eski hafiza kaldi: {yanit[-200:]}"
        return "yeni sohbet eski konuşmayı unuttu"
    finally:
        u.kapat()


def s_yanlis_model(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p], model="boyle-bir-model-yok:1b")
    u = Uygulama(g / "v", kaynak)
    try:
        u.mesaj("merhaba", sure=60)
        hatalar = [o.get("metin", "") for o in u.hepsi if o.get("tur") in ("hata", "surec_bitti")]
        assert hatalar, "hata gosterilmedi"
        u.komut({"tur": "ayar_kaydet", "ayar": {"model": MODEL}})
        u.bekle(lambda o: o.get("tur") == "model" and o.get("model") == MODEL, 20)
        u.mesaj("Yalnız 'tamam' yaz.", sure=120)
        yanit = "".join(o.get("metin", "") for o in u.hepsi if o.get("tur") == "icerik")
        assert yanit.strip(), "model degisince calismadi"
        return f"olmayan modelde anlaşılır hata ({hatalar[0][:60]}…), ayar değişince düzeldi"
    finally:
        u.kapat()


def s_korumali(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p], korumali=True, korumali_imaj="python:3.13-slim")
    u = Uygulama(g / "v", kaynak)
    try:
        u.mesaj("Şu komutu çalıştır ve çıktısını yaz: python --version", sure=240)
        cikti = "".join(o.get("metin", "") for o in u.hepsi if o.get("tur") == "sonuc")
        assert "3.13" in cikti, f"kutuda calismadi: {cikti[-200:]}"
        return "komut Docker kutusunda çalıştı (Python 3.13)"
    finally:
        u.kapat()


def s_turkce_yol(g: Path, kaynak: bool) -> str:
    a = proje(g / "İlk Proje", {"oku.md": "birinci\n"})
    b = proje(g / "Çalışma Şeması ğüş", HESAP)
    ayar(g / "v", [a, b])
    u = Uygulama(g / "v", kaynak)
    try:
        u.komut({"tur": "klasor_ac", "klasor": str(b)})
        u.bekle(lambda o: o.get("tur") == "klasor" and o.get("klasor") == str(b), 20)
        u.mesaj(DUZELT)
        assert "a + b" in (b / "hesap.py").read_text(encoding="utf-8"), "Turkce adli klasorde duzelmedi"
        u.komut({"tur": "klasor_ac", "klasor": str(g)})  # listede olmayan klasor acilamamali
        time.sleep(2)
        assert not any(o.get("tur") == "klasor" and o.get("klasor") == str(g) for o in u.hepsi), "bilinmeyen klasor acildi"
        return "Türkçe ve boşluklu klasörde çalıştı; listede olmayan klasör açılamadı"
    finally:
        u.kapat()


def s_kapanis(g: Path, kaynak: bool) -> str:
    p = proje(g / "p", HESAP)
    ayar(g / "v", [p])
    u = Uygulama(g / "v", kaynak)
    u.akisi_kes()
    bas = time.time()
    try:
        u.surec.wait(60)
    except subprocess.TimeoutExpired:
        u.surec.kill()
        raise AssertionError("pencere kapaninca program kapanmadi")
    return f"pencere kapanınca program {time.time() - bas:.0f} sn'de kapandı"


SENARYOLAR = {"temel": s_temel, "red": s_red, "geri_al": s_geri_al, "dur": s_dur, "gizli": s_gizli, "anilan": s_anilan,
              "kalicilik": s_kalicilik, "yeni": s_yeni, "yanlis_model": s_yanlis_model, "korumali": s_korumali,
              "turkce_yol": s_turkce_yol, "kapanis": s_kapanis}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ay = argparse.ArgumentParser()
    ay.add_argument("--kaynak", action="store_true", help="exe yerine uygulama.py")
    ay.add_argument("--sadece", help="virgulle senaryo adlari")
    s = ay.parse_args()
    if not s.kaynak and not EXE.is_file():
        print(f"{EXE} yok; once masaustu/paketle_exe.py", file=sys.stderr)
        return 2
    secili = s.sadece.split(",") if s.sadece else list(SENARYOLAR)
    basarisiz = 0
    for ad in secili:
        g = Path(tempfile.mkdtemp(prefix="ka-uu-"))
        bas = time.time()
        try:
            sonuc = SENARYOLAR[ad](g, s.kaynak)
            print(f"GECTI  {ad:13} {time.time() - bas:5.0f} sn  {sonuc}", flush=True)
        except Exception as hata:
            basarisiz += 1
            print(f"KALDI  {ad:13} {time.time() - bas:5.0f} sn  {type(hata).__name__}: {hata}", flush=True)
        finally:
            for _ in range(10):  # git nesneleri salt okunur; ajan sureci kapanana kadar klasor kilitli olabilir
                try:
                    shutil.rmtree(g, onexc=lambda f, yol, _h: (os.chmod(yol, 0o666), f(yol)))
                except OSError:
                    pass
                if not g.exists():
                    break
                time.sleep(1)
    print(f"{len(secili) - basarisiz}/{len(secili)} senaryo geçti")
    return 1 if basarisiz else 0


if __name__ == "__main__":
    sys.exit(main())
