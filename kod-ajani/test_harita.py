import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a


class TanimTesti(unittest.TestCase):
    def test_python_imzalari(self):
        kod = "async def al(x: int, y=1) -> str:\n    def ic(): pass\nclass K(Taban):\n    def m(self, a): pass\nSABIT = 1\ndeger = 2\n"
        t = a.dosya_tanimlari("a.py", kod)
        self.assertEqual([x["ad"] for x in t], ["al", "K", "m", "SABIT"])
        self.assertEqual(t[0]["imza"], "async def al(x: int, y=1)")
        self.assertEqual(t[1]["imza"], "class K(Taban)")
        self.assertEqual(t[2]["derinlik"], 1)

    def test_bozuk_python_haritayi_kirmaz(self):
        # Ayristirilamayan Python dosyasi duzenli ifadeyle okunur.
        self.assertEqual([x["ad"] for x in a.dosya_tanimlari("a.py", "def iyi(:\n    pass\n def sonra(x):\n")], ["iyi", "sonra"])

    def test_diger_diller(self):
        ornekler = {
            "a.ts": ("export async function al(x: number) {\nexport class K {\nconst f = (a) => a\nif (x) {\n", ["al", "K", "f"]),
            "a.go": ("func Al(x int) {\nfunc (s *S) M() {\ntype S struct {\n", ["Al", "M", "S"]),
            "a.rs": ("pub fn al() {\nstruct S {\nimpl S {\n", ["al", "S"]),
            "A.java": ("public class A {\n  public int al(int x) {\n  return 1;\n", ["A", "al"]),
            "a.c": ("static int al(int x)\n{\nstruct s {\nif (x) {\n", ["al", "s"]),
        }
        for ad, (kod, beklenen) in ornekler.items():
            self.assertEqual([x["ad"] for x in a.dosya_tanimlari(ad, kod)], beklenen, ad)

    def test_bilinmeyen_uzanti_bos(self):
        self.assertEqual(a.dosya_tanimlari("a.txt", "def x(): pass"), [])


@unittest.skipUnless(a._ts_ayristirici("javascript") and a._ts_ayristirici("c_sharp"), "tree-sitter kurulu degil")
class TreeSitterTesti(unittest.TestCase):
    def test_ornek_dosyalarin_tum_tanimlari(self):
        import harita_ornekleri as h
        for o in h.ORNEKLER:
            with self.subTest(o["yol"]):
                self.assertEqual({t["ad"] for t in a.dosya_tanimlari(o["yol"], o["metin"])}, o["beklenen"])

    def test_imza_ve_ust(self):
        import harita_ornekleri as h
        cs = {t["ad"]: t for t in a.dosya_tanimlari(h.ORNEKLER[2]["yol"], h.ORNEKLER[2]["metin"])}
        self.assertEqual(cs["Toplam"]["imza"], "public decimal Toplam(IEnumerable<decimal> fiyatlar)")
        self.assertEqual(cs["Toplam"]["ust"]["ad"], "SiparisServisi")
        self.assertTrue(cs["OlusturAsync"]["imza"].startswith("public async Task<Siparis> OlusturAsync("), "oznitelik imzaya girmemeli")

    def test_adli_fonksiyonun_ici_girmez_adsiz_sarmalayicinin_girer(self):
        js = ("function dis() {\n  const yerel = () => 1;\n  return yerel();\n}\n"
              "(function () {\n  function panelKur() {}\n  const durum = () => 2;\n})();\n"
              "describe('x', () => {\n  it('y', () => { const taklit = { yaz: () => 1 }; });\n});\n"
              "foo({ secenek: () => 1 });\n")
        self.assertEqual({t["ad"] for t in a.dosya_tanimlari("a.js", js)}, {"dis", "panelKur", "durum"})

    def test_bozuk_dosya_da_patlamaz(self):
        self.assertIsInstance(a.dosya_tanimlari("a.cs", "public class A { void B( { "), list)

    def test_tree_sitter_yoksa_duzenli_ifade(self):
        with patch.object(a, "_ts_ayristirici", return_value=None):
            adlar = {t["ad"] for t in a.dosya_tanimlari("a.js", "export function topla(a, b) {\n  return a + b;\n}\n")}
        self.assertEqual(adlar, {"topla"})


class HaritaTesti(unittest.TestCase):
    def setUp(self):
        self.kok = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.kok, ignore_errors=True)

    def yaz(self, ad, icerik):
        y = self.kok / ad
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_text(icerik, encoding="utf-8")

    def harita(self, istek="", butce=4000, onbellek=None):
        dosyalar = sorted(p.relative_to(self.kok).as_posix() for p in self.kok.rglob("*") if p.is_file())
        return a.proje_haritasi(self.kok, dosyalar, istek, butce, onbellek)

    def test_cok_kullanilan_once_gelir(self):
        self.yaz("cekirdek.py", "def ortak_islem(x):\n    return x\n")
        for i in range(5):
            self.yaz(f"m{i}.py", f"from cekirdek import ortak_islem\ndef kullan{i}():\n    return ortak_islem(1)\n")
        h = self.harita()
        self.assertTrue(h.startswith("cekirdek.py:"), h)
        self.assertIn("1: def ortak_islem(x)", h)

    def test_metotla_birlikte_sinifi_gorunur(self):
        self.yaz("a.py", "class Kasa:\n" + "".join(f"    def yardim{i}(self): pass\n" for i in range(30)) +
                 "    def ozel_odeme(self): pass\n")
        for i in range(5):
            self.yaz(f"k{i}.py", "def kullan(k):\n    k.ozel_odeme(); k.ozel_odeme()\n")
        h = self.harita(butce=70)
        self.assertIn("ozel_odeme", h)
        self.assertIn("class Kasa", h)
        self.assertLess(h.index("class Kasa"), h.index("ozel_odeme"))

    def test_butceye_uyar(self):
        for i in range(50):
            self.yaz(f"d{i}.py", "".join(f"def f{i}_{j}(a, b, c):\n    pass\n" for j in range(20)))
        for butce in (200, 1000, 4000):
            h = self.harita(butce=butce)
            self.assertLessEqual(len(h), butce)
            self.assertGreater(len(h), butce * 0.5)

    def test_istekte_gecen_dosya_ve_ad_one_cikar(self):
        self.yaz("sepet.py", "def toplam_hesapla():\n    pass\n")
        self.yaz("stok.py", "def stok_dus():\n    pass\n")
        for i in range(4):
            self.yaz(f"s{i}.py", f"from stok import stok_dus\ndef g{i}():\n    stok_dus()\n")
        self.assertTrue(self.harita(butce=4000).startswith("stok.py:"))
        h = self.harita("sepet dosyasindaki toplam_hesapla bozuk", butce=4000)
        self.assertLess(h.index("toplam_hesapla"), h.index("stok_dus"))

    def test_bos_veya_kodsuz_proje(self):
        self.assertEqual(self.harita(), "")
        self.yaz("notlar.txt", "merhaba\n")
        self.assertEqual(self.harita(), "")

    def test_onbellek_yalniz_degisen_dosyayi_okur(self):
        self.yaz("a.py", "def a1(): pass\n")
        self.yaz("b.py", "def b1(): pass\n")
        onb = {}
        self.harita(onbellek=onb)
        with patch.object(a, "metin_oku", side_effect=AssertionError("okunmamaliydi")):
            self.harita(onbellek=onb)
        self.yaz("a.py", "def a_uzun_yeni_ad(): pass\n")
        self.assertIn("a_uzun_yeni_ad", self.harita(onbellek=onb))

    def test_buyuk_proje_makul_surede(self):
        for i in range(300):
            self.yaz(f"p/m{i}.py", "".join(f"def f{i}_{j}(a):\n    return f{(i + 1) % 300}_{j}(a)\n" for j in range(20)))
        bas = time.time()
        h = self.harita(butce=4000)
        self.assertLess(time.time() - bas, 15)
        self.assertLessEqual(len(h), 4000)


class AjanTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.gecici, ignore_errors=True)
        self.kok = self.gecici / "proje"
        self.kok.mkdir()
        (self.kok / "a.py").write_text("def ozel_islem():\n    pass\n", encoding="utf-8")
        ortam = patch.dict(os.environ, {"KOD_AJANI_VERI": str(self.gecici / "veri")})
        ortam.start()
        self.addCleanup(ortam.stop)

    def yanitsiz(self, ajan):
        ajan._modeli_cagir = lambda: {"role": "assistant", "content": "tamam", "tool_calls": []}

    def test_harita_sistem_istemine_girer_ve_tazelenir(self):
        ajan = a.Ajan(self.kok, "sahte")
        self.yanitsiz(ajan)
        ajan.tur("selam")
        self.assertIn("1: def ozel_islem()", ajan.mesajlar[0]["content"])
        (self.kok / "a.py").write_text("def yeni_isim():\n    pass\n", encoding="utf-8")
        ajan.tur("yine")
        self.assertIn("yeni_isim", ajan.mesajlar[0]["content"])
        self.assertNotIn("ozel_islem", ajan.mesajlar[0]["content"])
        self.assertEqual(ajan.mesajlar[0]["content"].count("Project map"), 1)

    def test_kapatilabilir(self):
        ajan = a.Ajan(self.kok, "sahte", harita_butce=0)
        self.yanitsiz(ajan)
        ajan.tur("selam")
        self.assertNotIn("Project map", ajan.mesajlar[0]["content"])

    def test_gitignore_haritaya_girmez(self):
        (self.kok / ".gitignore").write_text("gizli.py\n", encoding="utf-8")
        (self.kok / "gizli.py").write_text("def gizli_islem(): pass\n", encoding="utf-8")
        ajan = a.Ajan(self.kok, "sahte")
        self.yanitsiz(ajan)
        ajan.tur("selam")
        self.assertNotIn("gizli_islem", ajan.mesajlar[0]["content"])

    def test_harita_alinamazsa_tur_devam_eder(self):
        ajan = a.Ajan(self.kok, "sahte")
        self.yanitsiz(ajan)
        with patch.object(ajan.noktalar, "izlenen", side_effect=a.GeriAlmaHatasi("git yok")):
            self.assertTrue(ajan.tur("selam"))
        self.assertNotIn("Project map", ajan.mesajlar[0]["content"])

    def test_yeni_sohbet_temiz_baslar(self):
        ajan = a.Ajan(self.kok, "sahte")
        self.yanitsiz(ajan)
        ajan.tur("selam")
        ajan.sifirla()
        self.assertNotIn("Project map", ajan.mesajlar[0]["content"])


if __name__ == "__main__":
    unittest.main()
