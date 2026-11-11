#!/usr/bin/env python3
"""Gercek modelle bir tur calistirir, geri alir, yeniden uygular ve her adimi olcer.

Onay kurali deneme.py ile aynidir; her sey gecici bir kopyada olur.
"""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402
import deneme as d  # noqa: E402


def icerikler(kok: Path) -> dict:
    return {p.name: p.read_bytes() for p in kok.iterdir() if p.is_file()}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    gecici = Path(tempfile.mkdtemp())
    os.environ["KOD_AJANI_VERI"] = str(gecici / "veri")
    kok = gecici / "proje"
    kok.mkdir()
    try:
        d.proje_yaz(kok)
        once = icerikler(kok)
        arayuz = d.DenemeArayuzu()
        ajan = a.Ajan(kok, sys.argv[1] if len(sys.argv) > 1 else "gpt-oss:20b", maks_adim=25, arayuz=arayuz)
        basarili, nokta, dosyalar = ajan.tur_noktali(d.GOREV)
        sonra = icerikler(kok)
        tur = d.olc(kok)
        guvenlik, geri_dosyalar = ajan.geri_al(nokta)
        geri = icerikler(kok)
        geri_olc = d.olc(kok)
        ajan.geri_al(guvenlik)
        yeniden = icerikler(kok)
        print(json.dumps({
            "tur_basarili": basarili,
            "tur_gecen": f"{tur['gecen']}/{tur['toplam']}",
            "degisen": dosyalar,
            "geri_alinan_sayi": len(geri_dosyalar),
            "geri_alinca_baslangicla_ayni": geri == once,
            "geri_alinca_gecen": f"{geri_olc['gecen']}/{geri_olc['toplam']}",
            "yeniden_uygulayinca_ayni": yeniden == sonra,
            "gecmise_not_dustu": "reverted" in ajan.mesajlar[-1]["content"],
            "reddedilen": arayuz.kayit["reddedilen"],
        }, ensure_ascii=False, indent=2))
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
