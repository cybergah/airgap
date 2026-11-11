#!/usr/bin/env python3
"""Proje haritasinin JS/TS/C# ornek dosyalarinda ne kadar dogru tanim buldugunu olcer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402
import harita_ornekleri as h  # noqa: E402


def olc(ornekler=h.ORNEKLER, ayrinti=True) -> tuple[int, int, int]:
    dogru_top = beklenen_top = yanlis_top = 0
    for o in ornekler:
        bulunan = {t["ad"] for t in a.dosya_tanimlari(o["yol"], o["metin"])}
        dogru = bulunan & o["beklenen"]
        eksik = o["beklenen"] - bulunan
        yanlis = bulunan - o["beklenen"]
        dogru_top += len(dogru)
        beklenen_top += len(o["beklenen"])
        yanlis_top += len(yanlis)
        if ayrinti:
            print(f"{o['yol']}: buldu {len(dogru)}/{len(o['beklenen'])}, yanlis {len(yanlis)}")
            if eksik:
                print("   kacirdi:", ", ".join(sorted(eksik)))
            if yanlis:
                print("   yanlis :", ", ".join(sorted(yanlis)))
    print(f"TOPLAM: buldu {dogru_top}/{beklenen_top}, yanlis {yanlis_top}, yontem: {a.harita_yontemi()}")
    return dogru_top, beklenen_top, yanlis_top


if __name__ == "__main__":
    olc()
