#!/usr/bin/env python3
"""Turkce istekte model search_code'u kullaniyor mu, sorguyu nasil yaziyor, dogru dosyayi buluyor mu?

Yalnizca okuma araclari calisir: yazma ve komut istekleri reddedilir.
"""
import json
import os
import shutil
import sys
import sysconfig
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402
import deneme as d  # noqa: E402

SORULAR = [
    ("Bu projede bir listenin en büyük n elemanını hepsini sıralamadan bulan kod hangi dosyada? Sadece dosya adını söyle.", "heapq.py"),
    ("Uzun paragrafı satır genişliğine göre bölen kod nerede? Sadece dosya adını söyle.", "textwrap.py"),
    ("Parola için güvenli rastgele belirteç üreten kod hangi dosyada? Sadece dosya adını söyle.", "secrets.py"),
    ("Günlük dosyasını boyutu geçince döndüren kod nerede? Sadece dosya adını söyle.", "logging/handlers.py"),
    ("Sıralı listeye sırayı bozmadan eleman ekleyen kod nerede? Sadece dosya adını söyle.", "bisect.py"),
]


class Kayit(d.DenemeArayuzu):
    def __init__(self):
        super().__init__()
        self.cagrilar = []

    def arac(self, ad, arg):
        self.cagrilar.append([ad, arg])

    def sor(self, soru):
        return "h"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    kaynak = Path(sysconfig.get_paths()["stdlib"])
    gecici = Path(tempfile.mkdtemp())
    os.environ["KOD_AJANI_VERI"] = str(gecici / "veri")
    kok = gecici / "proje"
    kok.mkdir()
    dogru = 0
    try:
        # Dosya adlari cevabi ele vermesin: model icerige gore bulmak zorunda kalsin.
        kaynaklar = ["heapq.py", "textwrap.py", "secrets.py", "bisect.py", "shutil.py", "csv.py", "gzip.py",
                     "argparse.py", "logging/handlers.py", "http/client.py"]
        ad_haritasi = {ad: f"modul_{i:02d}.py" for i, ad in enumerate(kaynaklar)}
        for ad, yeni in ad_haritasi.items():
            shutil.copy(kaynak / ad, kok / yeni)
        for soru, hedef in [(s, ad_haritasi[h]) for s, h in SORULAR]:
            arayuz = Kayit()
            ajan = a.Ajan(kok, "gpt-oss:20b", maks_adim=8, arayuz=arayuz)
            ajan.tur(soru)
            yanit = (ajan.mesajlar[-1].get("content") or "") if ajan.mesajlar[-1]["role"] == "assistant" else ""
            buldu = hedef.split("/")[-1] in yanit
            dogru += buldu
            print(json.dumps({"hedef": hedef, "buldu": buldu, "yanit": yanit[:80],
                              "aramalar": [c[1].get("query") for c in arayuz.cagrilar if c[0] == "search_code"],
                              "diger_araclar": [c[0] for c in arayuz.cagrilar if c[0] != "search_code"]},
                             ensure_ascii=False), flush=True)
        print(f"OZET: {dogru}/{len(SORULAR)}")
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
