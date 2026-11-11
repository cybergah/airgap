import shutil
import tempfile
import unittest
from pathlib import Path

import ajan as a
from test_sunucu import Oturum


class TemizlemeTesti(unittest.TestCase):
    def test_duz_kod_oldugu_gibi_kalir(self):
        self.assertEqual(a.secim_temizle("x = 2", "x = 1"), "x = 2")

    def test_cit_kaldirilir(self):
        self.assertEqual(a.secim_temizle("```python\nx = 2\n```", "x = 1"), "x = 2")
        self.assertEqual(a.secim_temizle("```\nx = 2\ny = 3\n```\n", "x = 1"), "x = 2\ny = 3")

    def test_icerideki_cit_bozulmaz(self):
        kod = 'a = "```"\nb = 1'
        self.assertEqual(a.secim_temizle(kod, "x"), kod)

    def test_girinti_korunur(self):
        self.assertEqual(a.secim_temizle("    x = 2", "    x = 1"), "    x = 2")

    def test_model_girintiyi_atarsa_geri_konur(self):
        self.assertEqual(a.secim_temizle("if a:\n    b()\n\nc()", "    x = 1\n    y = 2"),
                         "    if a:\n        b()\n\n    c()")

    def test_fazla_girinti_kesilmez(self):
        self.assertEqual(a.secim_temizle("        x = 2", "    x = 1"), "        x = 2")

    def test_secimin_satir_sonu_korunur(self):
        self.assertEqual(a.secim_temizle("x = 2", "x = 1\n"), "x = 2\n")
        self.assertEqual(a.secim_temizle("x = 2\n", "x = 1"), "x = 2")

    def test_windows_satir_sonlari(self):
        self.assertEqual(a.secim_temizle("x = 2\ny = 3", "x = 1\r\ny = 1\r\n"), "x = 2\r\ny = 3\r\n")

    def test_dusunce_etiketi_atilir(self):
        self.assertEqual(a.secim_temizle("<think>hmm</think>x = 2", "x = 1"), "x = 2")


class SecimSunucuTesti(unittest.TestCase):
    def setUp(self):
        self.kok = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.kok, ignore_errors=True)

    def oturum(self, yanitlar):
        o = Oturum(self.kok, yanitlar)
        self.addCleanup(o.kapat)
        o.bekle("hazir")
        return o

    def test_sonuc_doner_dosyaya_yazmaz_gecmise_girmez(self):
        (self.kok / "a.py").write_bytes(b"x = 1\n")
        o = self.oturum([[{"message": {"content": "```python\nx = 2\n```"}, "done": True}]])
        o.gonder(tur="secim", id=7, istek="iki yap", secim="x = 1", once="# önce", sonra="# sonra", yol="a.py", dil="python")
        sonuc = o.bekle("secim_sonuc")
        self.assertEqual((sonuc["id"], sonuc["yeni"]), (7, "x = 2"))
        self.assertEqual((self.kok / "a.py").read_bytes(), b"x = 1\n")
        istek = o.sunucu.istekler[0]
        self.assertNotIn("tools", istek)
        metin = istek["messages"][1]["content"]
        for parca in ("iki yap", "x = 1", "# önce", "# sonra", "a.py"):
            self.assertIn(parca, metin)
        o.gonder(tur="mesaj", metin="selam")
        o.bekle("tur_bitti")
        sonraki = [m["content"] for m in o.sunucu.istekler[-1]["messages"]]
        self.assertFalse([m for m in sonraki if "iki yap" in m])

    def test_bos_ve_uzun_secim_model_cagirmadan_reddedilir(self):
        o = self.oturum([])
        o.gonder(tur="secim", id=1, istek="x", secim="   ")
        self.assertIn("bos", o.bekle("secim_sonuc")["hata"])
        o.gonder(tur="secim", id=2, istek="x", secim="a" * (a.SECIM_SINIRI + 1))
        self.assertIn("uzun", o.bekle("secim_sonuc")["hata"])
        self.assertEqual(o.sunucu.istekler, [])

    def test_bos_yanit_hata_olur(self):
        o = self.oturum([[{"message": {"content": "```\n```"}, "done": True}]])
        o.gonder(tur="secim", id=1, istek="x", secim="y")
        self.assertIn("hata", o.bekle("secim_sonuc"))

    def test_model_hatasi_oturumu_oldurmez(self):
        o = self.oturum([])
        o.sunucu.shutdown()
        o.sunucu.server_close()
        o.gonder(tur="secim", id=1, istek="x", secim="y")
        self.assertIn("Ollama", o.bekle("secim_sonuc")["hata"])
        self.assertIsNone(o.surec.poll())
        o.sunucu.shutdown = lambda: None
        o.sunucu.server_close = lambda: None


if __name__ == "__main__":
    unittest.main()
