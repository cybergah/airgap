#!/usr/bin/env python3
"""Ayni dosyalarda eski (duzenli ifade) ve yeni (tree-sitter) haritanin buldugu tanimlari karsilastirir.

Kullanim: python harita_karsilastir.py dosya1.js dosya2.cs ...   (veya @liste.txt)
Dogruluk icin elle bakilir: yalniz birinin buldugu adlar listelenir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402


def tanimlar(yol: Path, tree_sitter: bool) -> set[str]:
    metin = a.metin_oku(yol)
    if tree_sitter:
        return {t["ad"] for t in a.dosya_tanimlari(str(yol), metin)}
    eski = a._ts_tanimlari
    a._ts_tanimlari = lambda *x: None
    try:
        return {t["ad"] for t in a.dosya_tanimlari(str(yol), metin)}
    finally:
        a._ts_tanimlari = eski


def main(yollar: list[str]) -> None:
    if len(yollar) == 1 and yollar[0].startswith("@"):
        yollar = [s.strip().lstrip("﻿") for s in Path(yollar[0][1:]).read_text(encoding="utf-8").splitlines() if s.strip()]
    eski_top = yeni_top = ortak_top = 0
    for y in yollar:
        yol = Path(y)
        try:
            eski, yeni = tanimlar(yol, False), tanimlar(yol, True)
        except (OSError, a.AracHatasi):
            continue
        eski_top += len(eski)
        yeni_top += len(yeni)
        ortak_top += len(eski & yeni)
        if "-a" in sys.argv[0:0] or len(yollar) <= 10:
            print(f"{yol.name}: eski {len(eski)}, yeni {len(yeni)}, ortak {len(eski & yeni)}")
            if yeni - eski:
                print("   yalniz yeni:", ", ".join(sorted(yeni - eski)[:25]))
            if eski - yeni:
                print("   yalniz eski:", ", ".join(sorted(eski - yeni)[:25]))
    print(f"TOPLAM {len(yollar)} dosya: eski {eski_top}, yeni {yeni_top}, ortak {ortak_top}")


if __name__ == "__main__":
    main(sys.argv[1:])
