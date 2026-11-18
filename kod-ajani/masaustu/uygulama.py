"""Airgap masaustu: VS Code olmadan, Edge uygulama penceresinde ayni ajan ve sohbet.

    python masaustu/uygulama.py            # gelistirme
    Airgap.exe                             # paketlenmis hali (paketle_exe.py)

Yapi: yalniz 127.0.0.1'de dinleyen kucuk bir HTTP sunucusu paneli (vscode-eklenti/media) sunar; Edge bunu
--app kipinde adres cubugu olmayan bir pencerede acar. Ajan, eklentideki gibi `ajan.py --sunucu` alt surecidir
ve satir basina bir JSON konusur. Sunucuya her istek rastgele bir anahtar ve Host denetimi ister: baska bir
web sayfasi ya da yerel program onay veremez, komut gonderemez.
"""
from __future__ import annotations

import hashlib
import json
import re
import os
import queue
import secrets
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

DONDURULMUS = getattr(sys, "frozen", False)
KAYNAK = Path(getattr(sys, "_MEIPASS", "")) if DONDURULMUS else Path(__file__).resolve().parent.parent
MASAUSTU = KAYNAK / "masaustu"
ARAYUZ = MASAUSTU / "arayuz" / "dist"  # React arayuzu (npm run build)
VERI = Path(os.environ.get("KOD_AJANI_MASAUSTU_VERI") or Path(os.environ.get("APPDATA") or Path.home()) / "kod-ajani" / "masaustu")
AYAR_DOSYASI = VERI / "ayarlar.json"
VARSAYILAN_AYAR = {"model": "gpt-oss:20b", "gomme": "", "dusunme": "", "baglam": 16384, "maks_adim": 40,
                   "harita_butcesi": 1000, "korumali": False, "korumali_imaj": "python:3.13-slim", "dil": "",
                   "son_klasorler": []}
YAYIN_SURESI = 8  # pencere kapandiktan sonra bekleme; sayfa yenilenirken (F5) akis bu kadar kopuk kalmaz
CANLI_ARALIK = 4  # olay akisina bos satir araligi: kopan pencere en gec bu kadar saniyede anlasilir
TURLER = {".js": "application/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".html": "text/html",
          ".woff2": "font/woff2"}
# Shiki renkleri ve React stil nitelikleri satir ici stil ister; betik yalniz kendi kaynagimizdan.
CSP = ("default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; "
       "font-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")  # kucuk yazi tipleri gomulu
SESSIZ = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def ollama_adresi() -> str:
    """OLLAMA_HOST sunucunun dinledigi adrestir; 0.0.0.0 ("her yerde dinle") baglanilacak adres degildir."""
    adres = (os.environ.get("OLLAMA_HOST") or "127.0.0.1:11434").strip().rstrip("/")
    if "://" not in adres:
        adres = "http://" + adres
    p = urlparse(adres)
    makine = p.hostname or "127.0.0.1"
    if makine in ("0.0.0.0", "::", "[::]"):
        makine = "127.0.0.1"
    return f"{p.scheme}://{makine}:{p.port or 11434}"


OLLAMA = ollama_adresi()


def sistem_dili() -> str:
    """Windows arayuz dili Turkce ise "tr", degilse "en" (Airgap'in varsayilani Ingilizce)."""
    try:
        if os.name == "nt":
            import ctypes
            return "tr" if ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF == 0x1F else "en"
        import locale
        return "tr" if (locale.getlocale()[0] or "").lower().startswith("tr") else "en"
    except Exception:
        return "en"


def guvenli_yaz(hedef: Path, metin: str) -> None:
    """Gecici dosyaya yazip yerine koyar. Windows'ta virus tarayicisi yeni dosyayi bir an kilitleyebilir
    (os.replace PermissionError verir); birkac kez yeniden denenir."""
    hedef.parent.mkdir(parents=True, exist_ok=True)
    gecici = hedef.with_name(f"{hedef.name}.{threading.get_ident()}.tmp")  # her is parcacigina ayri
    gecici.write_text(metin, encoding="utf-8")
    for deneme in range(20):
        try:
            os.replace(gecici, hedef)
            return
        except PermissionError:
            if deneme == 19:
                gecici.unlink(missing_ok=True)
                raise
            time.sleep(0.05 * (deneme + 1))


def ayar_oku() -> dict:
    try:
        kayitli = json.loads(AYAR_DOSYASI.read_text(encoding="utf-8-sig"))  # elle duzenlenip BOM eklenmis olabilir
    except (OSError, ValueError):
        kayitli = {}
    return {**VARSAYILAN_AYAR, **(kayitli if isinstance(kayitli, dict) else {})}


def ayar_yaz(ayar: dict) -> None:
    guvenli_yaz(AYAR_DOSYASI, json.dumps(ayar, ensure_ascii=False, indent=2))


def gecmis_dosyasi(klasor: str) -> Path:
    ad = hashlib.sha1(os.path.normcase(os.path.abspath(klasor)).encode("utf-8")).hexdigest()[:16]
    return VERI / "gecmis" / f"{ad}.json"


DOSYA_SINIRI = 5000


def proje_dosyalari(klasor: str) -> list[str]:
    """@ onerileri icin proje dosyalari; ajanin atladigi klasorler ve gizli dosyalar (.env, anahtar) yok."""
    sys.path.insert(0, str(KAYNAK))
    import ajan
    kok = Path(klasor)
    liste: list[str] = []
    for yer, altlar, dosyalar in os.walk(kok):
        altlar[:] = sorted(a for a in altlar if a not in ajan.ATLANAN_KLASORLER and not a.startswith("."))
        for ad in sorted(dosyalar):
            goreli = (Path(yer) / ad).relative_to(kok).as_posix()
            if not ajan.gizli_mi(goreli):
                liste.append(goreli)
                if len(liste) >= DOSYA_SINIRI:
                    return liste
    return liste


def ajan_komutu() -> list[str]:
    if DONDURULMUS:
        return [sys.executable, "--ajan"]
    return [sys.executable, "-B", str(KAYNAK / "ajan.py")]


class Uygulama:
    def __init__(self):
        self.ayar = ayar_oku()
        self.anahtar = secrets.token_urlsafe(24)
        self.kilit = threading.RLock()
        self.dinleyiciler: list[queue.Queue] = []
        self.son_baglanti = time.time()
        self.klasor: str | None = None
        self.gecmis: list[dict] = []
        self.surec: subprocess.Popen | None = None
        self.mesgul = False
        self.saglik = {"tur": "saglik", "ollama": None}
        klasorler = [k for k in self.ayar.get("son_klasorler", []) if os.path.isdir(k)]
        if klasorler:
            self.klasor_ac(klasorler[0], yayinla=False)

    def dil(self) -> str:
        """Ayardaki dil; bossa AIRGAP_LANG (ajanla ayni kural), o da yoksa Windows'un dili."""
        if self.ayar.get("dil") in ("tr", "en"):
            return self.ayar["dil"]
        ortam = (os.environ.get("AIRGAP_LANG") or os.environ.get("KOD_AJANI_DIL") or "").strip().lower()
        if ortam:
            return "tr" if ortam.startswith(("tr", "tur", "türk")) else "en"
        return sistem_dili()

    def L(self, tr: str, en: str) -> str:
        return tr if self.dil() == "tr" else en

    def saglik_denetle(self) -> None:
        """Ollama'yi duzenli yoklar; durum degisince panele bildirir (kenar cubugundaki nokta)."""
        import urllib.request
        while True:
            try:
                with urllib.request.urlopen(OLLAMA + "/api/version", timeout=3) as y:
                    yeni = {"tur": "saglik", "ollama": True, "surum": json.loads(y.read()).get("version", "")}
            except Exception:
                yeni = {"tur": "saglik", "ollama": False}
            if yeni != self.saglik:
                self.saglik = yeni
                self.yayinla(yeni, kaydet=False)
            time.sleep(8)

    # ------------------------------------------------------------ panel olaylari
    def yayinla(self, olay: dict, kaydet: bool = True) -> None:
        with self.kilit:
            if kaydet:
                self.gecmis.append(olay)
                if len(self.gecmis) > 5000:
                    self.gecmis = self.gecmis[-4000:]
            for q in list(self.dinleyiciler):
                q.put(olay)

    def ajan_olayi(self, olay: dict) -> None:
        tur = olay.get("tur")
        if tur == "tur_bitti":
            self.mesgul = False
            self.yayinla(olay)
            self.gecmis_kaydet()
            return
        if tur == "surec_bitti":
            self.mesgul = False
        if tur == "degisiklik":
            olay = {k: v for k, v in olay.items() if k not in ("eski", "yeni")}  # panel farki gosterir
        self.yayinla(olay)

    def gecmis_kaydet(self) -> None:
        if not self.klasor:
            return
        with self.kilit:
            saklanan = [o for o in self.gecmis if o.get("tur") != "ayrac"][-1500:]
            metin = json.dumps(saklanan, ensure_ascii=False)
        try:
            guvenli_yaz(gecmis_dosyasi(self.klasor), metin)
        except OSError as hata:  # kayit yapilamadi diye sohbet durmasin
            self.yayinla({"tur": "uyari", "metin": self.L("Sohbet geçmişi kaydedilemedi: ", "Could not save chat history: ") + str(hata)}, kaydet=False)

    # ------------------------------------------------------------ proje klasoru
    def klasor_ac(self, klasor: str, yayinla: bool = True) -> None:
        klasor = os.path.abspath(klasor)
        self.ajan_kapat()
        with self.kilit:
            self.klasor = klasor
            try:
                kayitli = json.loads(gecmis_dosyasi(klasor).read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                kayitli = []
            self.gecmis = []
            if isinstance(kayitli, list) and kayitli:
                self.gecmis = [*kayitli, {"tur": "tur_bitti", "basarili": False},
                               {"tur": "ayrac", "metin": self.L("Önceki oturum · ajan bu sohbeti hatırlıyor", "Previous session · the agent remembers this chat")}]
            son = [klasor] + [k for k in self.ayar.get("son_klasorler", []) if os.path.normcase(k) != os.path.normcase(klasor)]
            self.ayar["son_klasorler"] = son[:10]
            ayar_yaz(self.ayar)
        if yayinla:
            self.yayinla({"tur": "temizle"}, kaydet=False)
            self.yayinla({"tur": "klasor", "klasor": klasor, "ad": Path(klasor).name}, kaydet=False)
            self.yayinla(self.projeler_olayi(), kaydet=False)
            for olay in list(self.gecmis):
                self.yayinla(olay, kaydet=False)

    def projeler_olayi(self) -> dict:
        liste = [{"klasor": k, "ad": Path(k).name or k} for k in self.ayar.get("son_klasorler", []) if os.path.isdir(k)]
        return {"tur": "projeler", "liste": liste}

    def klasor_sec(self) -> None:
        """Windows klasor secme penceresi; ayri is parcaciginda acilir, sunucu beklemez."""
        def sec():
            try:
                import tkinter
                from tkinter import filedialog
                kok = tkinter.Tk()
                kok.withdraw()
                kok.attributes("-topmost", True)
                secilen = filedialog.askdirectory(parent=kok, title=self.L("Airgap: proje klasörünü seç", "Airgap: choose the project folder"),
                                                  initialdir=self.klasor or str(Path.home()), mustexist=True)
                kok.destroy()
            except Exception as hata:  # tkinter yoksa ya da pencere acilamadiysa
                self.yayinla({"tur": "hata", "metin": self.L("Klasör seçme penceresi açılamadı: ", "Could not open the folder picker: ") + str(hata)}, kaydet=False)
                return
            if secilen:
                self.klasor_ac(secilen)
        threading.Thread(target=sec, daemon=True).start()

    # ------------------------------------------------------------ ajan sureci
    def ajan_baslat(self) -> bool:
        if self.surec and self.surec.poll() is None:
            return True
        if not self.klasor:
            self.yayinla({"tur": "hata", "metin": self.L("Önce bir proje klasörü seç.", "Choose a project folder first.")})
            return False
        a = self.ayar
        argumanlar = ajan_komutu() + ["--sunucu", "--model", str(a["model"]), "--dizin", self.klasor,
                                      "--baglam", str(a["baglam"]), "--maks-adim", str(a["maks_adim"]),
                                      "--harita-butce", str(a["harita_butcesi"])]
        if a.get("gomme"):
            argumanlar += ["--gomme-modeli", str(a["gomme"])]
        if a.get("dusunme") in ("low", "medium", "high", "uyarlanir"):
            argumanlar += ["--dusunme-seviyesi", a["dusunme"]]
        if a.get("korumali"):
            argumanlar += ["--korumali", str(a.get("korumali_imaj") or "python:3.13-slim")]
        if any(o.get("tur") == "kullanici" for o in self.gecmis):
            argumanlar.append("--sohbet-yukle")
        ortam = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "AIRGAP_LANG": self.dil(), "KOD_AJANI_DIL": self.dil()}
        try:
            surec = subprocess.Popen(argumanlar, cwd=self.klasor, env=ortam, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, creationflags=SESSIZ)
        except OSError as hata:
            self.yayinla({"tur": "surec_bitti", "metin": self.L("Ajan başlatılamadı: ", "Could not start the agent: ") + str(hata)})
            return False
        self.surec = surec
        threading.Thread(target=self._oku, args=(surec,), daemon=True).start()
        threading.Thread(target=self._gunluk, args=(surec,), daemon=True).start()
        return True

    def _oku(self, surec: subprocess.Popen) -> None:
        for satir in surec.stdout:
            try:
                olay = json.loads(satir.decode("utf-8", "replace"))
            except ValueError:
                continue
            if isinstance(olay, dict):
                self.ajan_olayi(olay)
        kod = surec.wait()
        if self.surec is surec:
            self.surec = None
            self.ajan_olayi({"tur": "surec_bitti", "metin": self.L(f"Ajan süreci kapandı (kod {kod}). Ayrıntı: {VERI / 'ajan.log'}", f"The agent process exited (code {kod}). Details: {VERI / 'ajan.log'}")})

    def _gunluk(self, surec: subprocess.Popen) -> None:
        VERI.mkdir(parents=True, exist_ok=True)
        with open(VERI / "ajan.log", "ab") as f:
            for satir in surec.stderr:
                f.write(satir)
                f.flush()

    def ajana(self, komut: dict) -> bool:
        if not self.ajan_baslat():
            return False
        try:
            self.surec.stdin.write((json.dumps(komut, ensure_ascii=False) + "\n").encode("utf-8"))
            self.surec.stdin.flush()
            return True
        except OSError:
            return False

    def ajan_kapat(self) -> None:
        surec, self.surec = self.surec, None
        if surec and surec.poll() is None:
            try:
                surec.stdin.close()
                surec.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                surec.kill()

    # ------------------------------------------------------------ panelden gelen
    def panel_mesaji(self, m: dict) -> None:
        tur = m.get("tur")
        if tur == "acildi":
            q = m.get("_kuyruk")
            if self.klasor:
                q.put({"tur": "klasor", "klasor": self.klasor, "ad": Path(self.klasor).name})
            else:
                q.put({"tur": "klasor_yok"})
            q.put(self.projeler_olayi())
            q.put({"tur": "model", "model": self.ayar["model"]})
            q.put({"tur": "dil", "dil": self.dil()})
            q.put(self.saglik)
            for olay in list(self.gecmis):
                q.put(olay)
        elif tur == "mesaj" and str(m.get("metin", "")).strip():
            self.yayinla({"tur": "kullanici", "metin": str(m["metin"])})
            self.mesgul = True
            if not self.ajana({"tur": "mesaj", "metin": str(m["metin"]), "baglam": None}):
                self.mesgul = False
                self.yayinla({"tur": "tur_bitti", "basarili": False})
        elif tur == "onay" and self.surec:
            if m.get("yanit") in ("e", "h", "t"):
                with self.kilit:  # yeniden yuklemede kararin gorunmesi icin gecmise yazilir, sayfaya yayinlanmaz
                    self.gecmis.append({"tur": "onay_yanit", "id": m.get("id"), "yanit": m["yanit"]})
            self.ajana({"tur": "onay", "id": m.get("id"), "yanit": m.get("yanit")})
        elif tur == "dur" and self.surec:
            self.ajana({"tur": "dur"})
        elif tur == "geri_al" and self.surec:
            self.ajana({"tur": "geri_al", "nokta": m.get("nokta")})
        elif tur == "klasor_sec":
            if self.mesgul:
                self.yayinla({"tur": "uyari", "metin": self.L("Ajan çalışırken klasör değiştirilemez; önce durdur.", "Stop the agent before switching folders.")}, kaydet=False)
            else:
                self.klasor_sec()
        elif tur == "klasor_ac":
            # Yalniz daha once kullanicinin sectigi klasorler: sayfa rastgele bir yolu actiramaz.
            istenen = os.path.normcase(os.path.abspath(str(m.get("klasor", ""))))
            bilinen = [k for k in self.ayar.get("son_klasorler", []) if os.path.normcase(os.path.abspath(k)) == istenen]
            if bilinen and os.path.isdir(bilinen[0]) and not self.mesgul:
                self.klasor_ac(bilinen[0])
        elif tur == "dosya_listesi" and self.klasor:
            m["_kuyruk"].put({"tur": "dosyalar", "klasor": self.klasor, "liste": proje_dosyalari(self.klasor)})
        elif tur == "goster" and self.klasor:
            # Dosyayi Gezgin'de secili gosterir; acmaz (bir .py ya da .bat dosyasini acmak onu calistirabilir).
            kok = Path(self.klasor).resolve()
            try:
                hedef = (kok / str(m.get("yol", ""))).resolve()
                hedef.relative_to(kok)
            except (OSError, ValueError):
                return
            if hedef.exists() and os.name == "nt":
                subprocess.Popen(["explorer.exe", f"/select,{hedef}"], creationflags=SESSIZ)
        elif tur == "bag_ac":
            adres = str(m.get("adres", ""))
            if re.fullmatch(r"https?://[^\s\"'<>]+", adres) and len(adres) < 2000:
                import webbrowser
                webbrowser.open(adres)
        elif tur == "yeni":
            if self.surec:
                self.ajana({"tur": "dur"})
                self.ajana({"tur": "yeni"})
            with self.kilit:
                self.gecmis = []
            self.gecmis_kaydet()
            self.yayinla({"tur": "temizle"}, kaydet=False)
        elif tur == "ayar_al":
            m["_kuyruk"].put({"tur": "ayarlar", "ayar": {k: v for k, v in self.ayar.items() if k != "son_klasorler"}})
        elif tur == "ayar_kaydet" and isinstance(m.get("ayar"), dict):
            yeni = dict(self.ayar)
            for k, v in m["ayar"].items():
                if k in VARSAYILAN_AYAR and k != "son_klasorler" and type(v) is type(VARSAYILAN_AYAR[k]):
                    yeni[k] = v
            self.ayar = yeni
            ayar_yaz(yeni)
            self.ajan_kapat()
            self.yayinla({"tur": "uyari", "metin": self.L("Ayarlar kaydedildi; ajan bir sonraki mesajda yeni ayarlarla başlar.", "Settings saved; the agent restarts with them on your next message.")},
                         kaydet=False)
            self.yayinla({"tur": "model", "model": yeni["model"]}, kaydet=False)
            self.yayinla({"tur": "dil", "dil": self.dil()}, kaydet=False)


def sayfa(uyg: Uygulama) -> bytes:
    giris = ARAYUZ / "index.html"
    if giris.is_file():
        return giris.read_text(encoding="utf-8").replace("__ANAHTAR__", uyg.anahtar).encode("utf-8")
    return derlenmemis_sayfa(uyg)


def derlenmemis_sayfa(uyg: Uygulama) -> bytes:
    """Arayuz derlenmemisse (gelistirme) ne yapilacagini soyleyen sayfa."""
    tr = "Arayüz derlenmemiş. kod-ajani/masaustu/arayuz klasöründe: npm ci ve npm run build"
    en = "The interface is not built. In kod-ajani/masaustu/arayuz run: npm ci, then npm run build"
    return (f"<!doctype html><meta charset=utf-8><title>Airgap</title>"
            f"<body style='background:#0d1117;color:#e6edf3;font:15px system-ui;padding:40px'>"
            f"<p>{uyg.L(tr, en)}</p>").encode("utf-8")


def isleyici(uyg: Uygulama, port: int):
    izinli_host = {f"127.0.0.1:{port}", f"localhost:{port}"}

    class Isleyici(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):  # konsol yok; sessiz
            pass

        def _gecerli(self) -> bool:
            if self.headers.get("Host") not in izinli_host:  # DNS yeniden baglama saldirisina karsi
                return False
            koken = self.headers.get("Origin")
            return koken is None or koken in {f"http://{h}" for h in izinli_host}

        def _anahtar_dogru(self) -> bool:
            q = parse_qs(urlparse(self.path).query)
            verilen = (q.get("t") or [""])[0] or self.headers.get("X-Anahtar", "")
            return secrets.compare_digest(verilen, uyg.anahtar)

        def _gonder(self, kod: int, govde: bytes, tur: str = "text/plain; charset=utf-8") -> None:
            self.send_response(kod)
            self.send_header("Content-Type", tur)
            self.send_header("Content-Length", str(len(govde)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(govde)

        def do_GET(self):
            if not self._gecerli():
                return self._gonder(403, b"yasak")
            yol = urlparse(self.path).path
            if yol == "/":
                if not self._anahtar_dogru():
                    return self._gonder(403, b"anahtar gerekli")
                return self._gonder(200, sayfa(uyg), "text/html; charset=utf-8")
            if yol == "/olaylar":
                return self._olaylar() if self._anahtar_dogru() else self._gonder(403, b"anahtar gerekli")
            for on_ek, klasor in (("/assets/", ARAYUZ / "assets"), ("/", ARAYUZ)):
                if yol.startswith(on_ek):
                    ad = yol[len(on_ek):]
                    hedef = (klasor / ad).resolve()
                    if "/" not in ad and hedef.parent == klasor.resolve() and hedef.suffix in TURLER and hedef.is_file():
                        return self._gonder(200, hedef.read_bytes(), TURLER[hedef.suffix] + "; charset=utf-8")
            self._gonder(404, b"yok")

        def do_POST(self):
            if not self._gecerli() or not self._anahtar_dogru() or urlparse(self.path).path != "/komut":
                return self._gonder(403, b"yasak")
            try:
                uzunluk = min(int(self.headers.get("Content-Length", "0")), 2_000_000)
                m = json.loads(self.rfile.read(uzunluk).decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                return self._gonder(400, b"bozuk")
            if not isinstance(m, dict):
                return self._gonder(400, b"bozuk")
            kuyruk = uyg.dinleyiciler[-1] if uyg.dinleyiciler else queue.Queue()
            m.pop("_kuyruk", None)
            m["_kuyruk"] = kuyruk
            try:
                uyg.panel_mesaji(m)
            except Exception:  # hicbir hata istegi cevapsiz birakmasin; ayrinti gunluge
                import traceback
                VERI.mkdir(parents=True, exist_ok=True)
                with open(VERI / "sunucu.log", "a", encoding="utf-8") as f:
                    traceback.print_exc(file=f)
                uyg.yayinla({"tur": "hata", "metin": uyg.L("Beklenmeyen bir hata oldu; ayrıntı sunucu.log dosyasında.", "Something went wrong; see sunucu.log for details.")}, kaydet=False)
                return self._gonder(500, b"hata")
            self._gonder(204, b"")

        def _olaylar(self):
            q: queue.Queue = queue.Queue()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            with uyg.kilit:
                uyg.dinleyiciler.append(q)
            try:
                while True:
                    try:
                        olay = q.get(timeout=CANLI_ARALIK)
                        veri = "data: " + json.dumps(olay, ensure_ascii=False) + "\n\n"
                    except queue.Empty:
                        veri = ": canli\n\n"
                    self.wfile.write(veri.encode("utf-8"))
                    self.wfile.flush()
                    uyg.son_baglanti = time.time()
            except OSError:
                pass
            finally:
                with uyg.kilit:
                    if q in uyg.dinleyiciler:
                        uyg.dinleyiciler.remove(q)
                uyg.son_baglanti = time.time()

    return Isleyici


class Sunucu(ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # Pencere kapanirken kopan baglantilar olagan; yalniz beklenmeyen hatalar gunluge yazilir.
        hata = sys.exc_info()[1]
        if isinstance(hata, (ConnectionError, TimeoutError)):
            return
        VERI.mkdir(parents=True, exist_ok=True)
        import traceback
        with open(VERI / "sunucu.log", "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)


def edge_yolu() -> str | None:
    adaylar = [shutil.which("msedge")]
    for ortam in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"):
        if os.environ.get(ortam):
            adaylar.append(str(Path(os.environ[ortam]) / "Microsoft" / "Edge" / "Application" / "msedge.exe"))
    return next((a for a in adaylar if a and os.path.isfile(a)), None)


def pencere_ac(adres: str) -> None:
    edge = edge_yolu()
    if edge:
        profil = VERI / "pencere"
        profil.mkdir(parents=True, exist_ok=True)
        subprocess.Popen([edge, f"--app={adres}", f"--user-data-dir={profil}", "--window-size=960,1040",
                          "--no-first-run", "--no-default-browser-check", "--disable-features=Translate",
                          "--disable-extensions"], creationflags=SESSIZ)
    else:  # Edge yoksa varsayilan tarayici
        import webbrowser
        webbrowser.open(adres)


def gizli_konsol() -> None:
    """Pencereli exe'nin konsolu yok: ajanin actigi her konsol programi (git, docker, powershell) Windows'ta yeni,
    gorunur bir konsol alir; ekranda pencere yanip soner ve bu konsollar kapanirken git CTRL_C ile olur
    (cikis kodu 0xC000013A; geri alma noktasi alinamiyordu). Her alt surec gizli konsolla baslar.
    VS Code eklentisinde ajan python.exe'dir ve gizli konsolu alt sureclere gecer; orada gerek yok."""
    if os.name != "nt" or not DONDURULMUS:
        return
    asil = subprocess.Popen.__init__

    def gizli(self, *a, **k):
        if len(a) < 12 and not k.get("creationflags"):
            k["creationflags"] = SESSIZ
        asil(self, *a, **k)

    subprocess.Popen.__init__ = gizli


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--ajan":  # paketlenmis exe ajanin kendisi olarak da calisir
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        gizli_konsol()
        sys.path.insert(0, str(KAYNAK))
        import ajan
        return ajan.main()
    uyg = Uygulama()
    threading.Thread(target=uyg.saglik_denetle, daemon=True).start()
    sunucu = Sunucu(("127.0.0.1", 0), None)
    port = sunucu.server_address[1]
    sunucu.RequestHandlerClass = isleyici(uyg, port)
    threading.Thread(target=sunucu.serve_forever, daemon=True).start()
    adres = f"http://127.0.0.1:{port}/?t={uyg.anahtar}"
    if os.environ.get("KOD_AJANI_PENCERE") == "0":  # deneme: pencere acma, adresi yaz
        VERI.mkdir(parents=True, exist_ok=True)
        (VERI / "adres.txt").write_text(adres, encoding="utf-8")  # pencereli exe'de stdout yok
        if sys.stdout:
            print(adres, flush=True)
    else:
        pencere_ac(adres)
    acilis = time.time()
    try:
        while True:
            time.sleep(2)
            bagli = bool(uyg.dinleyiciler)
            if not bagli and time.time() - max(uyg.son_baglanti, acilis) > (YAYIN_SURESI if uyg.son_baglanti > acilis else 90):
                break  # pencere kapandi (ya da hic acilamadi)
    except KeyboardInterrupt:
        pass
    uyg.ajan_kapat()
    uyg.gecmis_kaydet()
    sunucu.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
