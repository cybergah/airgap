#!/usr/bin/env python3
"""Secili kod duzenlemeyi gercek modelle olcer: sonuc calisiyor mu, cevresini bozuyor mu?

Modelin urettigi kod ayri bir surecte, gecici klasorde calistirilir.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402

ONCE = "import math\n\n\n"
SONRA = "\n\n\nprint('son')\n"
OLCUMLER = [
    ("Sıfıra bölmede 0 döndür", "def bol(a, b):\n    return a / b",
     "assert bol(6, 3) == 2; assert bol(1, 0) == 0"),
    ("add type hints", "def topla(a, b):\n    return a + b",
     "import inspect; assert topla(1, 2) == 3; assert inspect.signature(topla).parameters['a'].annotation is not inspect._empty"),
    ("Bunu liste üretecine çevir", "def kareler(n):\n    s = []\n    for i in range(n):\n        s.append(i * i)\n    return s",
     "import inspect; assert kareler(3) == [0, 1, 4]; assert '[' in inspect.getsource(kareler) and 'append' not in inspect.getsource(kareler)"),
    ("Değişkenin adını toplam yap", "def f(xs):\n    t = 0\n    for x in xs:\n        t += x\n    return t",
     "import inspect; assert f([1, 2]) == 3; assert 'toplam' in inspect.getsource(f)"),
    ("Negatif sayı gelirse ValueError fırlat", "def kok(x):\n    return math.sqrt(x)",
     "assert kok(4) == 2\ntry:\n    kok(-1)\n    raise SystemExit(1)\nexcept ValueError:\n    pass"),
    ("Türkçe açıklama (docstring) ekle", "def yarim(x):\n    return x / 2",
     "assert yarim(4) == 2; assert yarim.__doc__"),
    ("Sınıf içindeki bu metoda None kontrolü ekle, None gelirse 0 döndür",
     "    def uzunluk(self, m):\n        return len(m)",
     "assert K().uzunluk(None) == 0; assert K().uzunluk('ab') == 2"),
]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    model = sys.argv[1] if len(sys.argv) > 1 else "gpt-oss:20b"
    gecici = Path(tempfile.mkdtemp())
    os.environ["KOD_AJANI_VERI"] = str(gecici / "veri")
    kok = gecici / "proje"
    kok.mkdir()
    ajan = a.Ajan(kok, model)
    gecen = 0
    try:
        for istek, secim, denetim in OLCUMLER:
            sinif = secim.startswith("    ")
            once = ONCE + ("class K:\n" if sinif else "")
            bas = time.time()
            kayit = {"istek": istek[:40]}
            try:
                yeni = ajan.secim_duzenle(istek, secim, once, SONRA, "ornek.py", "python")
                dosya = kok / "ornek.py"
                dosya.write_text(once + yeni + SONRA + "\n" + denetim + "\n", encoding="utf-8")
                sonuc = subprocess.run([sys.executable, "-B", str(dosya)], capture_output=True, text=True,
                                       timeout=20, cwd=kok, stdin=subprocess.DEVNULL)
                tamam = sonuc.returncode == 0 and "son" in sonuc.stdout
                cit_kaldi = "```" in yeni
                cevre_tekrar = "print('son')" in yeni or "import math" in yeni
                kayit.update(gecti=tamam and not cit_kaldi and not cevre_tekrar, cit_kaldi=cit_kaldi, cevre_tekrar=cevre_tekrar)
                if not tamam:
                    kayit.update(hata=sonuc.stderr.strip().splitlines()[-1:] , yeni=yeni[:300])
            except (a.AracHatasi, a.ModelHatasi) as hata:
                kayit.update(gecti=False, hata=str(hata))
            kayit["sure_sn"] = round(time.time() - bas, 1)
            gecen += bool(kayit["gecti"])
            print(json.dumps(kayit, ensure_ascii=False), flush=True)
        print(f"OZET: {model}: {gecen}/{len(OLCUMLER)}")
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
