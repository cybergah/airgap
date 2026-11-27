"""Paketlenmis Airgap.exe'nin acilip arayuzu sundugunu dener; model, Ollama ya da pencere gerekmez.

    python masaustu/duman_exe.py              # ../dist/Airgap.exe
    python masaustu/duman_exe.py YOL/Airgap.exe

Exe gecici bir ayar klasoruyle, pencere acmadan (KOD_AJANI_PENCERE=0) baslar ve adresini adres.txt'ye yazar.
Betik ana sayfayi ve sayfanin istedigi bir dosyayi ister: ikisi de geliyorsa derlenen arayuz exe'nin icinde demektir.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

EXE = Path(__file__).resolve().parent.parent.parent / "dist" / "Airgap.exe"
BEKLEME = 60  # sn; tek dosyalik exe ilk acilista kendini gecici klasore acar


def getir(adres: str) -> tuple[int, str]:
    with urllib.request.urlopen(adres, timeout=10) as y:
        return y.status, y.read().decode("utf-8", "replace")


def main() -> int:
    exe = Path(sys.argv[1]) if len(sys.argv) > 1 else EXE
    if not exe.is_file():
        print(f"exe yok: {exe}", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as veri:
        ortam = {**os.environ, "KOD_AJANI_PENCERE": "0", "KOD_AJANI_MASAUSTU_VERI": veri}
        surec = subprocess.Popen([str(exe)], env=ortam, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            dosya = Path(veri) / "adres.txt"
            son = time.time() + BEKLEME
            while not dosya.exists():
                if surec.poll() is not None:
                    print(f"exe acilmadan kapandi (cikis kodu {surec.returncode})", file=sys.stderr)
                    return 1
                if time.time() > son:
                    print(f"exe {BEKLEME} sn icinde adres yazmadi", file=sys.stderr)
                    return 1
                time.sleep(0.5)
            adres = dosya.read_text(encoding="utf-8").strip()
            kod, sayfa = getir(adres)
            betik = re.search(r'<script[^>]+src="([^"]+)"', sayfa)
            if kod != 200 or not betik:
                print(f"ana sayfa beklenen gibi degil (HTTP {kod}):\n{sayfa[:500]}", file=sys.stderr)
                return 1
            kod, govde = getir(urljoin(adres, betik.group(1)))
            if kod != 200 or len(govde) < 1000:
                print(f"arayuz dosyasi gelmedi: {betik.group(1)} (HTTP {kod}, {len(govde)} harf)", file=sys.stderr)
                return 1
            print(f"tamam: {exe.name} acildi, sayfa ve {betik.group(1)} ({len(govde)} harf) geldi")
            return 0
        finally:
            # Tek dosyalik exe iki surec: acici ve asil uygulama. Yalniz aciciyi oldurmek uygulamayi acik birakir.
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(surec.pid)], capture_output=True)
            surec.kill()
            surec.wait(timeout=30)


if __name__ == "__main__":
    sys.exit(main())
