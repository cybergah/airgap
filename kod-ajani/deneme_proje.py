#!/usr/bin/env python3
"""Bir deneme projesini ajana panel kipinde sifirdan yaptirir ve gizli testlerle puanlar.

Proje gecici bir kopyadir. Onaylar kurallidir: kopyadaki dosya yazmalari onaylanir (ozel klasorler haric),
yalniz izinli komutlar (test ve uygulama komutlari, birkac salt okuma komutu) calisir, digerleri reddedilir.
Kullanim: python deneme_proje.py <proje> <degerlendir.py> <istek> [--tekrar N] [--model M]
"""
import argparse
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

BURASI = Path(__file__).resolve().parent
IZINLI_KOMUT = [
    r"node --test(?: [\w./\\-]+)*",
    r"node (?:\./)?cli\.js(?: (?:\"[^\"`$;&|<>]*\"|'[^'`$;&|<>]*'|[\w./:=,@ğüşıöçĞÜŞİÖÇ-]+))*",
    r"(?:dir|ls|Get-ChildItem)(?: -Recurse)?(?: [\w./\\-]+)?",
    r"(?:type|cat|Get-Content) [\w./\\-]+",
    r"node --version",
]


def izinli(komut: str) -> bool:
    k = komut.strip()
    # Proje disini gosteren yol (.., C:\, /etc, ~) hicbir izinli komutta kabul edilmez.
    if ".." in k or re.search(r"(?:^|\s)[/\\~]|[A-Za-z]:[\\/]", k):
        return False
    return any(re.fullmatch(d, k) for d in IZINLI_KOMUT)


def kos(proje: Path, istek: str, model: str, maks_adim: int, sure: int, korumali: str | None = None) -> dict:
    gecici = Path(tempfile.mkdtemp())
    kok = gecici / proje.name
    shutil.copytree(proje, kok, ignore=shutil.ignore_patterns(".git"))
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=kok, stdin=subprocess.DEVNULL, capture_output=True)
    ortam = dict(os.environ, KOD_AJANI_VERI=str(gecici / "veri"), PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    p = subprocess.Popen([sys.executable, "-B", str(BURASI / "ajan.py"), "--sunucu", "--model", model, "--dizin", str(kok),
                          "--maks-adim", str(maks_adim), *(["--korumali", korumali] if korumali else []),
                          *(["--dusunme-seviyesi", os.environ["KOD_AJANI_DUSUNME"]] if os.environ.get("KOD_AJANI_DUSUNME") else [])],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, env=ortam, cwd=kok, text=True, encoding="utf-8")
    olaylar: queue.Queue = queue.Queue()
    threading.Thread(target=lambda: [olaylar.put(json.loads(s)) for s in p.stdout if s.strip().startswith("{")],
                     daemon=True).start()
    yaz = lambda **k: (p.stdin.write(json.dumps(k, ensure_ascii=False) + "\n"), p.stdin.flush())
    kayit = {"komut_onay": [], "komut_red": [], "yazilan": [], "araclar": {}, "uyarilar": [], "balon": []}
    bekleyen = None
    bas = time.time()
    sonuc_tur = None
    simdiki = ""
    while time.time() - bas < sure:
        try:
            o = olaylar.get(timeout=5)
        except queue.Empty:
            if p.poll() is not None:
                break
            continue
        t = o["tur"]
        if t == "hazir":
            yaz(tur="mesaj", metin=istek)
        elif t == "arac":
            kayit["araclar"][o["ad"]] = kayit["araclar"].get(o["ad"], 0) + 1
        elif t == "komut":
            bekleyen = ("komut", o["komut"])
            kayit["araclar"]["run_command"] = kayit["araclar"].get("run_command", 0) + 1
        elif t == "degisiklik":
            bekleyen = ("yazma", o["yol"])
            kayit["araclar"][o["ad"]] = kayit["araclar"].get(o["ad"], 0) + 1
        elif t == "onay":
            tur, deger = bekleyen or ("", "")
            if tur == "komut":
                # Korumali kipte komut agi kapali, yetkisiz kapsayicida calisir: hepsi onaylanir ama kaydedilir.
                evet = bool(korumali) or izinli(deger)
                kayit["komut_onay" if evet else "komut_red"].append(deger[:160])
            elif tur == "yazma":
                evet = not re.match(r"^\.(git|vscode|github|idea|claude)/", deger)
                if evet:
                    kayit["yazilan"].append(deger)
            else:
                evet = False  # gizli dosya okuma
            yaz(tur="onay", id=o["id"], yanit="e" if evet else "h")
            bekleyen = None
        elif t == "uyari":
            kayit["uyarilar"].append(o.get("metin", "")[:160])
        elif t == "icerik":
            simdiki += o.get("metin", "")
        elif t == "ara_not":
            if simdiki:
                simdiki = ""
            elif kayit["balon"]:
                kayit["balon"].pop()
        elif t == "mesaj_bitti" and simdiki.strip():
            kayit["balon"].append(simdiki.strip())
            simdiki = ""
        elif t == "tur_bitti":
            sonuc_tur = o.get("basarili")
            break
    try:
        p.stdin.close()
        p.wait(timeout=30)
    except Exception:  # noqa: BLE001
        p.kill()
    kayit["sure_sn"] = round(time.time() - bas)
    kayit["tur_tamam"] = sonuc_tur
    kayit["son_cevap"] = (kayit["balon"][-1] if kayit["balon"] else "")[-600:]
    kayit["dosyalar"] = sorted(str(y.relative_to(kok)).replace("\\", "/") for y in kok.rglob("*")
                               if y.is_file() and ".git" not in y.parts and "node_modules" not in y.parts)
    kayit["kok"] = str(kok)
    return kayit


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a = argparse.ArgumentParser()
    a.add_argument("proje")
    a.add_argument("degerlendir")
    a.add_argument("istek")
    a.add_argument("--tekrar", type=int, default=1)
    a.add_argument("--model", default="gpt-oss:20b")
    a.add_argument("--maks-adim", type=int, default=40)
    a.add_argument("--sure", type=int, default=1200)
    a.add_argument("--korumali", help="Docker imaji: komutlar ve degerlendirme kapsayicida calisir (orn. node:22-slim)")
    s = a.parse_args()
    if s.korumali:
        os.environ["DEGERLENDIR_IMAJ"] = s.korumali
    ozet = []
    for i in range(1, s.tekrar + 1):
        print(f"\n######## DENEME {i}/{s.tekrar}", flush=True)
        k = kos(Path(s.proje).resolve(), s.istek, s.model, s.maks_adim, s.sure, s.korumali)
        print(json.dumps({x: k[x] for x in ("sure_sn", "tur_tamam", "araclar", "yazilan", "komut_onay", "komut_red", "dosyalar")},
                         ensure_ascii=False, indent=1))
        print("uyarilar:", k["uyarilar"][-6:])
        print("panelde balon sayisi:", len(k["balon"]))
        print("son cevap:", k["son_cevap"])
        d = subprocess.run([sys.executable, "-B", s.degerlendir, k["kok"]], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print(d.stdout[-2500:])
        gecen = re.search(r"ℹ pass (\d+)", d.stdout)
        toplam = re.search(r"ℹ tests (\d+)", d.stdout)
        ozet.append(f"{gecen.group(1) if gecen else '?'}/{toplam.group(1) if toplam else '?'}")
        shutil.rmtree(Path(k["kok"]).parent, ignore_errors=True)
    print("\nOZET gizli testler:", ozet, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
