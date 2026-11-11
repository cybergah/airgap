#!/usr/bin/env python3
"""Proje aramasini gercek gomme modeliyle olcer: dogru dosya ilk 1'de / ilk 5'te mi, ne kadar surdu.

Corpus olarak Python'un kendi standart kutuphanesinden bir kopya kullanilir; sorular
isim gecirmeden ne yapildigini anlatir, boylece yalnizca kelime eslemesi yetmez.
"""
import json
import os
import shutil
import sys
import sysconfig
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402

KLASORLER = ["email", "http", "json", "logging", "unittest", "urllib", "wsgiref", "xml", "sqlite3", "concurrency"]
DOSYALAR = ["argparse.py", "csv.py", "heapq.py", "shutil.py", "tempfile.py", "textwrap.py", "zipfile/__init__.py",
            "gzip.py", "difflib.py", "datetime.py", "_pydatetime.py", "secrets.py", "uuid.py", "base64.py", "bisect.py"]

SORULAR = [
    ("how to pick the n largest items from a list without sorting all of it", "heapq.py"),
    ("wrap a long paragraph so that each line fits a given width", "textwrap.py"),
    ("generate a random token that is safe to use for passwords", "secrets.py"),
    ("find the longest matching blocks between two sequences to show differences", "difflib.py"),
    ("copy a whole folder tree recursively to another location", "shutil.py"),
    ("compress a stream of bytes and write a checksum and file header", "gzip.py"),
    ("parse command line options and print a usage message", "argparse.py"),
    ("write rows to a comma separated file with quoting", "csv.py"),
    ("rotate log files when they get bigger than a size limit", "logging/handlers.py"),
    ("decode percent escapes in a web address", "urllib/parse.py"),
    ("send a request over a socket and read the status line and headers of the web response", "http/client.py"),
    ("skip a test unless a condition holds", "unittest/case.py"),
    ("create a temporary folder that is removed automatically", "tempfile.py"),
    ("insert into a sorted list keeping it sorted", "bisect.py"),
    ("encode binary data to a text form with sixty four characters", "base64.py"),
    ("break an email message into its attachments and mime parts", "email/"),
]


SORULAR_TR = [
    ("bir listenin en büyük n elemanını hepsini sıralamadan bulma", "heapq.py"),
    ("uzun bir paragrafı her satır belirli genişliğe sığacak şekilde bölme", "textwrap.py"),
    ("parola için güvenli rastgele belirteç üretme", "secrets.py"),
    ("iki metin arasındaki farkları bulma", "difflib.py"),
    ("bir klasör ağacını başka bir yere özyinelemeli kopyalama", "shutil.py"),
    ("komut satırı seçeneklerini ayrıştırma ve kullanım mesajı yazdırma", "argparse.py"),
    ("satırları virgülle ayrılmış dosyaya yazma", "csv.py"),
    ("günlük dosyası belirli boyutu geçince döndürme", "logging/handlers.py"),
    ("otomatik silinen geçici klasör oluşturma", "tempfile.py"),
    ("sıralı listeye sırayı bozmadan eleman ekleme", "bisect.py"),
]


def olc(dizin, sorular) -> dict:
    bir = bes = 0
    kacan = []
    for soru, hedef in sorular:
        yollar = [s["yol"] for s in dizin.ara(soru, adet=5)]
        sira = next((i + 1 for i, y in enumerate(yollar) if y.startswith(hedef)), None)
        bir += sira == 1
        bes += sira is not None
        if sira != 1:
            kacan.append({"soru": soru[:48], "hedef": hedef, "sira": sira, "ilk": yollar[0] if yollar else None})
    return {"soru": len(sorular), "ilk_1": bir, "ilk_5": bes, "kacan": kacan}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    model = sys.argv[1] if len(sys.argv) > 1 else "nomic-embed-text"
    kaynak = Path(sysconfig.get_paths()["stdlib"])
    gecici = Path(tempfile.mkdtemp())
    os.environ["KOD_AJANI_VERI"] = str(gecici / "veri")
    kok = gecici / "proje"
    kok.mkdir()
    try:
        for ad in KLASORLER:
            if (kaynak / ad).is_dir():
                shutil.copytree(kaynak / ad, kok / ad, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "test*"))
        for ad in DOSYALAR:
            if (kaynak / ad).is_file():
                (kok / ad).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(kaynak / ad, kok / ad)
        g = a.GeriAlma(kok)
        dizin = a.ProjeDizini(kok, g.izlenen, model)
        bas = time.time()
        ozet = dizin.guncelle()
        ilk = time.time() - bas
        bas = time.time()
        ikinci = dizin.guncelle()
        bos = time.time() - bas
        bir = bes = 0
        sureler, ayrinti = [], []
        for soru, hedef in SORULAR:
            b = time.time()
            sonuc = dizin.ara(soru, adet=5)
            sureler.append(time.time() - b)
            yollar = [s["yol"] for s in sonuc]
            sira = next((i + 1 for i, y in enumerate(yollar) if y.startswith(hedef)), None)
            bir += sira == 1
            bes += sira is not None
            ayrinti.append({"soru": soru[:48], "hedef": hedef, "sira": sira, "ilk": yollar[0] if yollar else None})
        sureler.sort()
        print(json.dumps({
            "model": model, "dizin": ozet, "ilk_dizinleme_sn": round(ilk, 1), "degisiksiz_guncelleme_sn": round(bos, 2),
            "degisiksiz_yeni": ikinci["yeni"], "soru": len(SORULAR), "ilk_1": bir, "ilk_5": bes,
            "ortanca_arama_sn": round(sureler[len(sureler) // 2], 2), "en_yavas_arama_sn": round(sureler[-1], 2),
            "dizin_mb": round(dizin.dosya.stat().st_size / 1e6, 1),
            "ingilizce": olc(dizin, SORULAR), "turkce": olc(dizin, SORULAR_TR),
        }, ensure_ascii=False, indent=1))
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
