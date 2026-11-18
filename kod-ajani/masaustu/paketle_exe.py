"""Masaustu uygulamasini tek dosyalik Airgap.exe yapar (PyInstaller gerekir: pip install pyinstaller).

    python masaustu/paketle_exe.py      # cikti: ../dist/Airgap.exe

Exe hem pencereyi acar hem de `Airgap.exe --ajan ...` olarak ajanin kendisi calisir; Python kurulu olmasi gerekmez.
"""
import subprocess
import sys
from pathlib import Path

BURASI = Path(__file__).resolve().parent
KOK = BURASI.parent
AYRAC = ";" if sys.platform == "win32" else ":"


def arayuzu_derle() -> int:
    """React arayuzunu derler (masaustu/arayuz/dist). npm ve node_modules gerekir: once `npm ci`."""
    arayuz = BURASI / "arayuz"
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    if not (arayuz / "node_modules").is_dir():
        print("arayuz/node_modules yok: once masaustu/arayuz icinde `npm ci` calistir.", file=sys.stderr)
        return 1
    return subprocess.call([npm, "run", "build"], cwd=arayuz)


def main() -> int:
    if arayuzu_derle() != 0:
        return 1
    veri = [(BURASI / "arayuz" / "dist", "masaustu/arayuz/dist")]
    komut = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
             "--name", "Airgap", "--icon", str(BURASI / "simge" / "airgap.ico"), "--paths", str(KOK), "--hidden-import", "ajan",
             "--distpath", str(KOK.parent / "dist"), "--workpath", str(KOK / "build" / "masaustu"),
             "--specpath", str(KOK / "build")]
    for kaynak, hedef in veri:
        komut += ["--add-data", f"{kaynak}{AYRAC}{hedef}"]
    komut.append(str(BURASI / "uygulama.py"))
    return subprocess.call(komut)


if __name__ == "__main__":
    sys.exit(main())
