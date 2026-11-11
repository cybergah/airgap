"""User-interface language: English by default, Turkish with AIRGAP_LANG=tr.

Only what the user sees is translated; what the model receives must not change.
"""
import os
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a

KAYNAK = Path(a.__file__).read_text(encoding="utf-8")
TURKCE = re.compile(r"[çğıöşüÇĞİÖŞÜ]")


def dil(deger):
    return patch.dict(os.environ, {"AIRGAP_LANG": deger, "KOD_AJANI_DIL": ""})


class DilSecimi(unittest.TestCase):
    def test_varsayilan_ingilizce(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AIRGAP_LANG", None)
            os.environ.pop("KOD_AJANI_DIL", None)
            self.assertEqual(a.arayuz_dili(), "en")
            self.assertEqual(a.L("evet", "yes"), "yes")

    def test_turkce_secilebilir(self):
        for deger in ("tr", "TR", "tr_TR", "turkish"):
            with dil(deger):
                self.assertEqual(a.arayuz_dili(), "tr")
                self.assertEqual(a.L("evet", "yes"), "evet")

    def test_eski_degisken_de_calisir(self):
        with patch.dict(os.environ, {"AIRGAP_LANG": "", "KOD_AJANI_DIL": "tr"}):
            self.assertEqual(a.arayuz_dili(), "tr")


class RiskCevirisi(unittest.TestCase):
    def test_her_risk_nedeninin_ingilizcesi_var(self):
        # Kaynakta risk listesine eklenen ve kural tablolarindaki tum nedenler.
        nedenler = set(re.findall(r'riskler\.append\("([^"]+)"\)', KAYNAK))
        nedenler |= {n for _, n in a._DERLI_RISK} | {n for _, n in a._DERLI_SUPHELI_NOT}
        nedenler |= set(re.findall(r'nedenler\.append\("([^"]+)"\)', KAYNAK))
        nedenler |= set(re.findall(r'return "", \["([^"]+)"\]', KAYNAK))
        self.assertGreater(len(nedenler), 15)
        eksik = sorted(n for n in nedenler if TURKCE.search(n) and n not in a.RISK_EN)
        self.assertEqual(eksik, [], "RISK_EN is missing translations")

    def test_ingilizce_karsiliklar_turkce_harf_icermez(self):
        for tr, en in a.RISK_EN.items():
            with self.subTest(tr=tr):
                self.assertIsNone(TURKCE.search(en))

    def test_uyari_secili_dilde(self):
        riskler = a.komut_riskleri("Remove-Item -Recurse x")
        self.assertTrue(riskler)
        with dil("en"):
            self.assertEqual(a.risk_metni(riskler[0]), a.RISK_EN[riskler[0]])
        with dil("tr"):
            self.assertEqual(a.risk_metni(riskler[0]), riskler[0])


class EkranCevirisi(unittest.TestCase):
    def test_hata_mesaji_cevrilir(self):
        with dil("en"):
            self.assertEqual(a.ekran_sonucu("HATA: dosya bulunamadi: x.py"), "ERROR: file not found: x.py")
            self.assertEqual(a.ekran_metni("klasor bulunamadi: src"), "folder not found: src")
        with dil("tr"):
            self.assertEqual(a.ekran_sonucu("HATA: dosya bulunamadi: x.py"), "HATA: dosya bulunamadi: x.py")

    def test_komut_ciktisi_ve_dosya_icerigi_degismez(self):
        icerik = "1\tprint('dosya bulunamadi: x')\n2\t# klasor bulunamadi"
        with dil("en"):
            self.assertEqual(a.ekran_sonucu(icerik), icerik)
            self.assertEqual(a.ekran_sonucu("ok\n[cikis kodu: 0]"), "ok\n[exit code: 0]")
            self.assertEqual(a.ekran_sonucu("(sonuc yok)"), "(no results)")
            self.assertEqual(a.ekran_sonucu("a.py duzenlendi"), "a.py edited")

    def test_modele_giden_sonuc_cevrilmez(self):
        """Arac sonucu modele Turkce kalir: dil ayari ajanin davranisini degistirmez."""
        import tempfile
        with tempfile.TemporaryDirectory() as d, dil("en"):
            araclar = a.Araclar(Path(d))
            sonuc = araclar.calistir("read_file", {"path": "yok.py"})
            self.assertTrue(sonuc.startswith("HATA: dosya bulunamadi"))


class TerminalArayuzu(unittest.TestCase):
    def test_ingilizce_yanitlar_kabul_edilir(self):
        ui = a.TerminalArayuz()
        for giris, beklenen in (("y", "e"), ("yes", "e"), ("n", "h"), ("no", "h"), ("a", "t"), ("all", "t")):
            with self.subTest(giris=giris), dil("en"), patch("builtins.input", return_value=giris):
                self.assertEqual(ui.sor("Run?"), beklenen)

    def test_yardim_iki_dilde(self):
        self.assertIn("/undo", a.YARDIM_EN)
        self.assertIn("/geri", a.YARDIM)
        self.assertIsNone(TURKCE.search(a.YARDIM_EN))


if __name__ == "__main__":
    unittest.main()
