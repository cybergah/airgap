import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a


class GeriAlmaTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.gecici, ignore_errors=True)
        self.kok = self.gecici / "proje"
        self.kok.mkdir()
        ortam = patch.dict(os.environ, {"KOD_AJANI_VERI": str(self.gecici / "veri")})
        ortam.start()
        self.addCleanup(ortam.stop)
        self.g = a.GeriAlma(self.kok)

    def yaz(self, ad, icerik):
        yol = self.kok / ad
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_bytes(icerik)

    def oku(self, ad):
        return (self.kok / ad).read_bytes()

    def test_degisen_silinen_eklenen_dosyalar_geri_doner(self):
        self.yaz("a.py", b"eski\n")
        self.yaz("sil.py", b"silinecek\n")
        nokta = self.g.nokta_al("once")
        self.yaz("a.py", b"yeni\n")
        (self.kok / "sil.py").unlink()
        self.yaz("alt/klasor/yeni.py", b"eklendi\n")
        self.assertEqual({(f["durum"], f["yol"]) for f in self.g.farklar(nokta)},
                         {("M", "a.py"), ("D", "sil.py"), ("A", "alt/klasor/yeni.py")})
        self.g.geri_al(nokta)
        self.assertEqual(self.oku("a.py"), b"eski\n")
        self.assertEqual(self.oku("sil.py"), b"silinecek\n")
        self.assertFalse((self.kok / "alt").exists())
        self.assertEqual(self.g.farklar(nokta), [])

    def test_geri_alma_da_geri_alinabilir(self):
        self.yaz("a.py", b"eski\n")
        nokta = self.g.nokta_al("once")
        self.yaz("a.py", b"yeni\n")
        self.yaz("ek.py", b"ek\n")
        guvenlik, _ = self.g.geri_al(nokta)
        self.assertEqual(self.oku("a.py"), b"eski\n")
        self.g.geri_al(guvenlik)
        self.assertEqual(self.oku("a.py"), b"yeni\n")
        self.assertEqual(self.oku("ek.py"), b"ek\n")

    def test_satir_sonlari_ve_turkce_ad_korunur(self):
        self.yaz("türkçe dosya.py", b"bir\r\niki\r\n")
        nokta = self.g.nokta_al("once")
        self.yaz("türkçe dosya.py", b"bozuk\n")
        self.assertEqual(self.g.farklar(nokta), [{"durum": "M", "yol": "türkçe dosya.py"}])
        self.g.geri_al(nokta)
        self.assertEqual(self.oku("türkçe dosya.py"), b"bir\r\niki\r\n")

    def test_kullanicinin_git_deposuna_dokunmaz(self):
        git = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
        subprocess.run([*git, "init", "-q"], cwd=self.kok, check=True)
        self.yaz("a.py", b"eski\n")
        subprocess.run([*git, "add", "."], cwd=self.kok, check=True)
        subprocess.run([*git, "commit", "-qm", "ilk"], cwd=self.kok, check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.kok, capture_output=True, text=True).stdout
        nokta = self.g.nokta_al("once")
        self.yaz("a.py", b"yeni\n")
        self.g.nokta_al("sonra")
        self.g.geri_al(nokta)
        kontrol = subprocess.run(["git", "status", "--short"], cwd=self.kok, capture_output=True, text=True)
        self.assertEqual(kontrol.stdout, "")
        self.assertEqual(subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.kok, capture_output=True,
                                        text=True).stdout, head)
        self.assertFalse(str(self.kok) in str(self.g.depo))

    def test_gitignore_dosyalari_silinmez(self):
        self.yaz(".gitignore", b"*.env\n")
        self.yaz("gizli.env", b"korunur\n")
        nokta = self.g.nokta_al("once")
        self.yaz("yeni.env", b"elle eklendi\n")
        self.g.geri_al(nokta)
        self.assertEqual(self.oku("gizli.env"), b"korunur\n")
        self.assertEqual(self.oku("yeni.env"), b"elle eklendi\n")

    def test_atlanan_klasorler_kaydedilmez_ve_silinmez(self):
        self.yaz("node_modules/x.js", b"buyuk\n")
        nokta = self.g.nokta_al("once")
        self.yaz("node_modules/y.js", b"yeni\n")
        self.assertEqual(self.g.farklar(nokta), [])
        self.g.geri_al(nokta)
        self.assertTrue((self.kok / "node_modules/y.js").exists())

    def test_gecersiz_nokta_hata_verir_dosyalara_dokunmaz(self):
        self.yaz("a.py", b"x\n")
        self.g.nokta_al("once")
        with self.assertRaises(a.GeriAlmaHatasi):
            self.g.geri_al("0" * 40)
        self.assertEqual(self.oku("a.py"), b"x\n")

    def test_ajan_gecmisine_not_duser(self):
        self.yaz("a.py", b"eski\n")
        ajan = a.Ajan(self.kok, "sahte")
        nokta = ajan.noktalar.nokta_al("once")
        self.yaz("a.py", b"yeni\n")
        ajan.geri_al(nokta)
        self.assertIn("a.py", ajan.mesajlar[-1]["content"])

    def test_git_yoksa_tur_yine_calisir(self):
        ajan = a.Ajan(self.kok, "sahte")
        ajan._modeli_cagir = lambda: {"role": "assistant", "content": "tamam", "tool_calls": []}
        with patch.object(ajan.noktalar, "nokta_al", side_effect=a.GeriAlmaHatasi("git bulunamadi")):
            basarili, nokta, dosyalar = ajan.tur_noktali("selam")
        self.assertTrue(basarili)
        self.assertIsNone(nokta)
        self.assertEqual(dosyalar, [])


if __name__ == "__main__":
    unittest.main()
