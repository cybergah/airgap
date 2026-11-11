import tempfile
import unittest
from pathlib import Path

import deneme as d


class DenemeTesti(unittest.TestCase):
    def setUp(self):
        gecici = tempfile.TemporaryDirectory()
        self.addCleanup(gecici.cleanup)
        self.kok = Path(gecici.name)
        d.proje_yaz(self.kok)

    def degistir(self, ad, eski, yeni):
        yol = self.kok / ad
        metin = yol.read_text(encoding="utf-8")
        self.assertIn(eski, metin)
        yol.write_text(metin.replace(eski, yeni), encoding="utf-8")

    def test_hatali_proje_bir_test_gecer(self):
        s = d.olc(self.kok)
        self.assertEqual((s["gecen"], s["toplam"]), (1, 7))
        self.assertFalse(s["indirim_fonksiyonu_duzeldi"])

    def test_dogru_cozum_yedi_test_gecer(self):
        self.degistir("urunler.py", "adet >= self.stok", "adet > self.stok")
        self.degistir("indirim.py", "KUPONLAR.get(kod, 0)", "KUPONLAR.get(kod.upper(), 0)")
        self.degistir("indirim.py", "fiyat * yuzde / 100", "fiyat * (100 - yuzde) / 100")
        self.degistir("sepet.py", "sum(urun.fiyat for", "sum(urun.fiyat * adet for")
        s = d.olc(self.kok)
        self.assertEqual((s["gecen"], s["toplam"]), (7, 7))
        self.assertTrue(s["indirim_fonksiyonu_duzeldi"])
        self.assertTrue(s["indirim_fonksiyonu_kullaniliyor"])

    def test_test_dosyasini_degistirmek_olcumu_kandirmaz(self):
        self.degistir("test_sepet.py", "toplam(), 250", "toplam(), 150")
        s = d.olc(self.kok)
        self.assertFalse(s["test_dosyasi_ayni"])
        self.assertEqual(s["gecen"], 1)

    def test_onay_kurali_dardir(self):
        arayuz = d.DenemeArayuzu()
        for tur, deger, beklenen in [
            ("komut", "python -B -m unittest", "e"),
            ("komut", "python -B -m unittest; del a.py", "h"),
            ("komut", "pip install x", "h"),
            ("degisiklik", "sepet.py", "e"),
            ("degisiklik", "test_sepet.py", "h"),
            ("degisiklik", "yeni.py", "h"),
        ]:
            arayuz.bekleyen = (tur, deger)
            self.assertEqual(arayuz.sor("?"), beklenen, deger)


if __name__ == "__main__":
    unittest.main()
