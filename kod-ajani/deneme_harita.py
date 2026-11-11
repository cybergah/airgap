#!/usr/bin/env python3
"""Proje haritasi gercekten ise yariyor mu? Ayni hatalari haritali ve haritasiz karsilastirir.

Python standart kutuphanesinden gecici bir kopyaya bilinen hatalar yerlestirilir. Gorevler
yalniz belirtiyi anlatir, dosya adi vermez. Basari, modelin kodu ayri bir surecte denetlenerek
olculur. Komut istekleri reddedilir; yalniz kopya icindeki .py duzenlemeleri onaylanir.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ajan as a  # noqa: E402
import deneme as d  # noqa: E402

DAGITICILAR = ["email", "http", "json", "logging", "urllib", "unittest", "argparse.py", "shutil.py", "tempfile.py",
               "csv.py", "gzip.py", "zipfile", "datetime.py", "_pydatetime.py", "uuid.py", "base64.py", "ipaddress.py",
               "configparser.py", "mimetypes.py", "shlex.py", "fnmatch.py", "statistics.py", "fractions.py"]

GOREVLER = [
    {"ad": "artik_yil", "dosya": "calendar.py",
     "eski": "year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)", "yeni": "year % 4 == 0 and year % 100 != 0",
     "gorev": "Bu projede bir hata var: 2000 yılı artık yıl sayılmıyor, oysa artık yıl. Hatayı bul ve düzelt. Komut çalıştırma, yalnız kodu düzelt.",
     "denetim": "import calendar as c; assert c.isleap(2000) and c.isleap(2024) and not c.isleap(1900) and not c.isleap(2023)"},
    {"ad": "baslik_harfi", "dosya": "string/__init__.py",
     "eski": "map(str.capitalize, s.split(sep))", "yeni": "map(str.lower, s.split(sep))",
     "gorev": "Bu projede bir hata var: cümledeki her kelimenin baş harfini büyüten yardımcı fonksiyon harfleri küçük bırakıyor. Hatayı bul ve düzelt. Komut çalıştırma, yalnız kodu düzelt.",
     "denetim": "import string as s; assert s.capwords('merhaba dunya') == 'Merhaba Dunya'"},
    {"ad": "html_kacis", "dosya": "html/__init__.py",
     "eski": 's = s.replace(">", "&gt;")', "yeni": 's = s.replace(">", "&lt;")',
     "gorev": "Bu projede bir hata var: metni web sayfası için güvenli hale getiren fonksiyon büyüktür işaretini yanlış karaktere çeviriyor. Hatayı bul ve düzelt. Komut çalıştırma, yalnız kodu düzelt.",
     "denetim": "import html; assert html.escape('<a>') == '&lt;a&gt;'"},
    {"ad": "tek_satir", "dosya": "textwrap.py",
     "eski": "w = TextWrapper(width=width, max_lines=1, **kwargs)", "yeni": "w = TextWrapper(width=width, max_lines=2, **kwargs)",
     "gorev": "Bu projede bir hata var: uzun metni belirli genişlikte tek satıra kısaltan fonksiyon bazen iki satır döndürüyor. Hatayı bul ve düzelt. Komut çalıştırma, yalnız kodu düzelt.",
     "denetim": "import textwrap as t; r = t.shorten('aaa bbb ccc ddd eee fff', width=8); assert '\\n' not in r, r"},
    {"ad": "benzerlik", "dosya": "difflib.py",
     "eski": "return 2.0 * matches / length", "yeni": "return 1.0 * matches / length",
     "gorev": "Bu projede bir hata var: iki metnin birbirine ne kadar benzediğini ölçen oran, birebir aynı metinler için 1 yerine 0.5 veriyor. Hatayı bul ve düzelt. Komut çalıştırma, yalnız kodu düzelt.",
     "denetim": "import difflib as x; assert x.SequenceMatcher(None, 'ab', 'ab').ratio() == 1.0; assert x.SequenceMatcher(None, 'ab', 'cd').ratio() == 0.0"},
]


class Kayit(d.DenemeArayuzu):
    def __init__(self):
        super().__init__()
        self.okunan: list[str] = []
        self.araclar: list[str] = []
        self.duzenlenen: list[str] = []

    def arac(self, ad, arg):
        self.araclar.append(ad)
        if ad == "read_file":
            self.okunan.append(str(arg.get("path")))

    def degisiklik(self, ad, yol, eski, yeni):
        self.bekleyen = ("degisiklik", yol)
        self.duzenlenen.append(yol)

    def komut(self, komut):
        self.bekleyen = ("komut", komut)

    def sor(self, soru):
        tur, deger = self.bekleyen
        izinli = tur == "degisiklik" and deger.endswith(".py")
        self.kayit["onaylanan" if izinli else "reddedilen"].append(f"{tur}: {str(deger)[:60]}")
        return "e" if izinli else "h"


def proje_kur(kok: Path) -> None:
    kaynak = Path(sysconfig.get_paths()["stdlib"])
    adlar = DAGITICILAR + [g["dosya"].split("/")[0] for g in GOREVLER]
    for ad in dict.fromkeys(adlar):
        k = kaynak / ad
        if k.is_dir():
            shutil.copytree(k, kok / ad, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "test*"))
        elif k.is_file():
            shutil.copy(k, kok / ad)
    for g in GOREVLER:
        y = kok / g["dosya"]
        metin = y.read_text(encoding="utf-8")
        assert metin.count(g["eski"]) == 1, f"hata yerlestirilemedi: {g['ad']}"
        y.write_text(metin.replace(g["eski"], g["yeni"]), encoding="utf-8")


def denetle(kok: Path, denetim: str) -> bool:
    p = subprocess.run([sys.executable, "-B", "-c", denetim], cwd=kok, capture_output=True, text=True, timeout=30,
                       stdin=subprocess.DEVNULL)
    return p.returncode == 0


def tek(g: dict, model: str, butce: int, maks_adim: int) -> dict:
    gecici = Path(tempfile.mkdtemp())
    os.environ["KOD_AJANI_VERI"] = str(gecici / "veri")
    kok = gecici / "proje"
    kok.mkdir()
    try:
        proje_kur(kok)
        assert not denetle(kok, g["denetim"]), f"yerlestirilen hata denetimde gorunmuyor: {g['ad']}"
        arayuz = Kayit()
        ajan = a.Ajan(kok, model, maks_adim=maks_adim, arayuz=arayuz, harita_butce=butce)
        bas = time.time()
        ajan.tur(g["gorev"])
        sure = round(time.time() - bas)
        return {"gorev": g["ad"], "harita": butce, "dogru": denetle(kok, g["denetim"]), "sure_sn": sure,
                "arac_sayisi": len(arayuz.araclar), "okunan": arayuz.okunan[:6], "duzenlenen": arayuz.duzenlenen[:6],
                "dogru_dosya_okundu": g["dosya"] in arayuz.okunan, "reddedilen": len(arayuz.kayit["reddedilen"]),
                "dusunce_karakter": arayuz.kayit["dusunce_karakter"], "uyari": arayuz.kayit["uyarilar"][-1:]}
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def main() -> int:
    for akis in (sys.stdout, sys.stderr):
        akis.reconfigure(encoding="utf-8", errors="replace")
    ay = argparse.ArgumentParser()
    ay.add_argument("--model", default="gpt-oss:20b")
    ay.add_argument("--tekrar", type=int, default=1)
    ay.add_argument("--maks-adim", type=int, default=15)
    ay.add_argument("--sure", type=int, default=240)
    ay.add_argument("--tek", help=argparse.SUPPRESS)
    ay.add_argument("--butce", type=int, default=1000)
    s = ay.parse_args()
    if s.tek:
        g = next(x for x in GOREVLER if x["ad"] == s.tek)
        print(json.dumps(tek(g, s.model, s.butce, s.maks_adim), ensure_ascii=False))
        return 0
    ozet = {0: [], 1000: []}
    for _ in range(s.tekrar):
        for g in GOREVLER:
            for butce in (1000, 0):  # ayni gorev peş peşe, sira etkisi az olsun
                try:
                    p = subprocess.run([sys.executable, "-B", __file__, "--tek", g["ad"], "--model", s.model,
                                        "--butce", str(butce), "--maks-adim", str(s.maks_adim)],
                                       capture_output=True, text=True, encoding="utf-8", timeout=s.sure)
                    r = json.loads(p.stdout.strip().splitlines()[-1]) if p.returncode == 0 and p.stdout.strip() else \
                        {"gorev": g["ad"], "harita": butce, "dogru": False, "hata": p.stderr[-400:]}
                except subprocess.TimeoutExpired:
                    r = {"gorev": g["ad"], "harita": butce, "dogru": False, "zaman_asimi": s.sure, "sure_sn": s.sure}
                ozet[butce].append(r)
                print(json.dumps(r, ensure_ascii=False), flush=True)
    for butce, ad in ((1000, "HARITALI"), (0, "HARITASIZ")):
        rs = ozet[butce]
        sureler = sorted(r.get("sure_sn", 0) for r in rs)
        print(f"OZET {ad}: dogru {sum(r['dogru'] for r in rs)}/{len(rs)}, "
              f"ortalama arac {sum(r.get('arac_sayisi', 0) for r in rs) / max(len(rs), 1):.1f}, "
              f"ortanca sure {sureler[len(sureler) // 2]} sn", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
