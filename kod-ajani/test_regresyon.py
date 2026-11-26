"""Otomatik test: yalniz duzenlemenin yeni bozdugu testler modele bildirilir."""
import unittest
from unittest.mock import patch

import ajan as a
from test_saglamlik import ModelTesti, yanit

PYTEST_ONCE = ("FAILED tests/test_pager.py::test_less[a- less] - FileNotFoundError: less\n"
               "ERROR tests/test_dep.py\n1 failed, 10 passed, 1 error in 1.00s\n[cikis kodu: 1]")
PYTEST_SONRA = PYTEST_ONCE.replace("1 failed", "2 failed").replace(
    "ERROR tests", "FAILED tests/test_types.py::test_range - click.BadParameter: 5 is not in the range\nERROR tests")


class BasarisizTestAdlariTesti(unittest.TestCase):
    def test_pytest_ve_unittest_ciktisi(self):
        self.assertEqual(a.basarisiz_testler(PYTEST_SONRA),
                         {"tests/test_pager.py::test_less[a- less]", "tests/test_dep.py", "tests/test_types.py::test_range"})
        cikti = "FAIL: test_x (test_a.T.test_x)\n----\nERROR: test_y (test_a.T)\nRan 2 tests\n[cikis kodu: 1]"
        self.assertEqual(a.basarisiz_testler(cikti), {"test_a.T.test_x.test_x", "test_a.T.test_y"})
        self.assertEqual(a.basarisiz_testler("OK\n[cikis kodu: 0]"), set())
        self.assertEqual(a.basarisiz_testler(cikti + "\nFAILED (failures=6, skipped=5)"), {"test_a.T.test_x.test_x", "test_a.T.test_y"},
                         "unittest ozet satiri test adi sayilmaz")


class RegresyonTesti(ModelTesti):
    DUZENLE = {"edit_file": {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}}

    def setUp(self):
        super().setUp()
        (self.kok / "test_a.py").write_text("import pytest\n", encoding="utf-8")
        self.ajan.araclar.kum = object()
        self.ajan._test_kumu = object()  # gercek kapsayici kurulmasin
        imaj = patch.object(a, "TEST_IMAJI", "sahte-test-imaji")
        imaj.start()
        self.addCleanup(imaj.stop)
        anlik = patch.object(a, "ANLIK_KONTROL", False)  # burada bitisteki otomatik test sinanir
        anlik.start()
        self.addCleanup(anlik.stop)
        self.komutlar = []

    def kur(self, once, *sonra):
        sira = iter(sonra)
        self.ajan._sessiz_komut = lambda komut: self.komutlar.append(komut) or once
        self.ajan._calistir_ve_bildir = lambda ad, arg: next(sira) if ad == "run_command" else "duzenlendi"

    def notlar(self):
        return [m["content"] for m in self.ajan.mesajlar if "[Automatic check]" in (m.get("content") or "")]

    def test_onceden_basarisiz_testler_bildirilmez(self):
        self.kur(PYTEST_ONCE, PYTEST_ONCE)
        self.kurgula(yanit(**self.DUZENLE), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual(self.notlar(), [])
        self.assertEqual(len(self.komutlar), 1, "ilk durum bir kez alinir")
        self.assertIn("pytest", self.komutlar[0])
        self.assertIn("--continue-on-collection-errors", self.komutlar[0])

    def test_yeni_bozulan_test_adiyla_bildirilir(self):
        self.kur(PYTEST_ONCE, PYTEST_SONRA, PYTEST_ONCE)
        self.kurgula(yanit(**self.DUZENLE), yanit("bitti"), yanit("duzelttim"))
        self.assertTrue(self.ajan.tur("isle"))
        notlar = self.notlar()
        self.assertEqual(len(notlar), 1)
        self.assertIn("- tests/test_types.py::test_range", notlar[0])
        self.assertNotIn("- tests/test_pager.py", notlar[0])
        self.assertEqual(self.ajan.mesajlar[-1]["content"], "duzelttim")

    def test_pytest_yoksa_unittest_e_doner(self):
        cevap = iter(["/usr/local/bin/python: No module named pytest\n[cikis kodu: 1]", "OK\n[cikis kodu: 0]"])
        self.ajan._sessiz_komut = lambda komut: self.komutlar.append(komut) or next(cevap)
        self.ajan._calistir_ve_bildir = lambda ad, arg: "OK\n[cikis kodu: 0]" if ad == "run_command" else "duzenlendi"
        self.kurgula(yanit(**self.DUZENLE), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual([("pytest" in k, "unittest" in k) for k in self.komutlar], [(True, False), (False, True)])

    def test_yavas_test_takimi_bu_turda_kapatilir(self):
        self.kur(f"...\n[{a.KOMUT_ZAMAN_ASIMI} saniyede bitmedigi icin durduruldu]", PYTEST_SONRA)
        self.kurgula(yanit(**self.DUZENLE), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual(self.notlar(), [])

    def test_src_duzeninde_yol_verilir(self):
        (self.kok / "src").mkdir()
        (self.kok / "src" / "m.py").write_text("y = 1\n", encoding="utf-8")
        self.assertTrue(self.ajan._test_komutu().startswith("PYTHONPATH=src python -B -m pytest"))
        with patch.object(a, "TEST_IMAJI", ""):
            self.assertEqual(self.ajan._test_komutu(), "python -B -m unittest", "test imaji yoksa eski komut")
        self.ajan.araclar.kum = None
        self.assertEqual(self.ajan._test_komutu(), "python -B -m unittest", "korumasiz ortamda eski, izinli komut")

    def test_ajanin_kosusu_test_kapsayicisinda_modelinki_asil_kapsayicida(self):
        asil, test = self.ajan.araclar.kum, self.ajan._test_kumu
        gorulen = []
        self.ajan.araclar.calistir = lambda ad, arg: gorulen.append(self.ajan.araclar.kum) or "OK"
        self.ajan._sessiz_komut("python -B -m pytest")
        self.assertIs(gorulen[0], test)
        self.assertIs(self.ajan.araclar.kum, asil, "sonra modelin kapsayicisina donulur")


if __name__ == "__main__":
    unittest.main()
