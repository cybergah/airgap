import tempfile
import unittest
from pathlib import Path

import olcum as o
import olcum_gorevleri as og


class GorevTesti(unittest.TestCase):
    def test_her_gorev_gecerli(self):
        for g in og.GOREVLER:
            with self.subTest(g["ad"]):
                self.assertEqual(o.gorev_dogrula(g), [])

    def test_adlar_benzersiz_turler_bilinen(self):
        adlar = [g["ad"] for g in og.GOREVLER]
        self.assertEqual(len(adlar), len(set(adlar)))
        self.assertLessEqual({g["tur"] for g in og.GOREVLER}, {"hata", "ozellik", "cok_dosya", "duzenleme", "soru", "tuzak"})

    def test_dolgu_ilgisiz_ve_cakismaz(self):
        for g in og.GOREVLER:
            self.assertFalse(set(og.dolgu_dosyalari(g.get("dolgu", 0))) & set(g["dosyalar"]), g["ad"])

    def test_soru_gorevlerinde_yanit_var(self):
        for g in og.GOREVLER:
            if g["tur"] == "soru":
                self.assertTrue(g["yanit_icerir"], g["ad"])

    def test_gizli_test_proje_dosyalarina_girmez(self):
        g = next(x for x in og.GOREVLER if x["ad"] == "ortalama")
        with tempfile.TemporaryDirectory() as k:
            o.proje_kur(g, Path(k))
            self.assertFalse((Path(k) / o.GIZLI_TEST).exists())


class PuanTesti(unittest.TestCase):
    def test_guven_araligi_kucuk_ornekte_genis(self):
        alt, ust = o.wilson(9, 10)
        self.assertLess(alt, 0.7)
        self.assertGreater(ust, 0.95)
        self.assertEqual(o.wilson(0, 0), (0.0, 0.0))
        alt2, ust2 = o.wilson(90, 100)
        self.assertGreater(alt2, alt)
        self.assertLess(ust2, ust)

    def test_ozet(self):
        s = [{"gorev": "a", "tur": "hata", "basari": True, "sure_sn": 10, "tur_tamam": True},
             {"gorev": "b", "tur": "hata", "basari": False, "sure_sn": 30, "tur_tamam": False, "zaman_asimi": True}]
        oz = o.ozet_hesapla(s)
        self.assertEqual((oz["basari"], oz["n"], oz["zaman_asimi"]), (1, 2, 1))
        self.assertEqual(oz["turler"]["hata"], [1, 2])

    def test_karsilastirma_kotuleseni_bulur(self):
        eski = [{"gorev": "a", "basari": True}, {"gorev": "b", "basari": False}, {"gorev": "c", "basari": True}]
        yeni = [{"gorev": "a", "basari": False}, {"gorev": "b", "basari": True}, {"gorev": "c", "basari": True}, {"gorev": "d", "basari": True}]
        f = o.karsilastir(yeni, eski)
        self.assertEqual((f["kotulesen"], f["iyilesen"], f["yalniz_yeni"], f["ortak_gorev"]), (["a"], ["b"], ["d"], 3))

    def test_onay_kurali(self):
        ar = o.OlcumArayuzu()
        ar.degisiklik("edit_file", "test_a.py", "", "")
        self.assertEqual(ar.sor("?"), "h")
        ar.degisiklik("edit_file", "a.py", "", "")
        self.assertEqual(ar.sor("?"), "e")
        ar.komut("rm -rf /")
        self.assertEqual(ar.sor("?"), "e")  # komutlar kapsayicida calisir
        self.assertEqual(ar.sor("Gizli dosya modele gonderilsin mi?"), "h")
        self.assertTrue(ar.kayit["gizli_okuma"])
        ar.arac("read_file", {"path": "a.py"})
        self.assertEqual(ar.kayit["arac_adlari"], {"edit_file": 2, "run_command": 1, "read_file": 1})
        self.assertEqual(ar.kayit["araclar"], 4)

    def test_hata_satiri_asil_hatayi_bulur(self):
        c = "Traceback\n  @onbellek\n   ^^^\nNameError: name 'x' is not defined\n\n---\nRan 1 test in 0.1s\n\nFAILED (errors=1)\n"
        self.assertEqual(o.hata_satiri(c), "NameError: name 'x' is not defined")
        self.assertEqual(o.hata_satiri("AssertionError: 1 != 2\nFAILED"), "AssertionError: 1 != 2")

    def test_erken_durma_dogru_adlandirilir(self):
        self.assertEqual(o.kisa_neden({"son_uyari": ["20 adim sinirina ulasildi, durduruldu."]}), "adım sınırı")
        self.assertEqual(o.kisa_neden({"son_uyari": ["Model x; tur durduruldu: y"]}), "ajan durdurdu: tekrar")
        self.assertEqual(o.kisa_neden({"hata_sayisi": 1}), "model hatası veya boş yanıt")
        self.assertEqual(o.kisa_neden({}), "tur tamamlanmadı")

    def test_itiraf_taninir(self):
        for m in ["Yapamadım", "çözemedim, yardım gerek", "test edilmedi", "I could not fix it", "doğrulanmadı", "unable to run"]:
            self.assertTrue(o.ITIRAF.search(m), m)
        for m in ["Testler geçiyor", "yardım çıktısı artık doğru sıralanacaktır", "fixed the bug", ""]:
            self.assertFalse(o.ITIRAF.search(m), m)

    def test_gereksiz_dosya_bulunur(self):
        g = {"hata": [("src/a.py", "x", "y")], "cozum": [("src/b.py", "x", "y")]}
        self.assertEqual(o.beklenmeyen_dosyalar(g, ["src/a.py", "src/b.py", "src/a.pyi", "tests/test_a.py", "cachetools/__init__.py", "tests/__init__.py"]),
                         ["cachetools/__init__.py", "tests/__init__.py"])
        self.assertEqual(o.beklenmeyen_dosyalar({}, ["x.py"]), [])

    def test_baglam_ozeti(self):
        o_ = [{"prompt_eval_count": 2200, "prompt_eval_duration": 5e8, "eval_count": 10, "eval_duration": 2e9},
              {"prompt_eval_count": 2300, "prompt_eval_duration": 1e7, "eval_count": 10, "eval_duration": 1e9},
              {"prompt_eval_count": 16000, "prompt_eval_duration": 3e9, "eval_count": 5, "eval_duration": 1e9}]
        oz = o.baglam_ozeti(o_, 16384)
        self.assertEqual((oz["cagri"], oz["okunan_en_fazla"], oz["baglama_dayandi"], oz["uretim_sn"]), (3, 16000, 1, 4.0))
        self.assertEqual(o.baglam_ozeti([], 16384)["okunan_en_fazla"], 0)

    def test_rapor_yazilir(self):
        s = [{"gorev": "a", "tur": "hata", "basari": True, "sure_sn": 1, "arac": 2, "tur_tamam": True}]
        v = {"etiket": "x", "tarih": "t", "model": "m", "tekrar": 1, "harita": 1000, "ozet": o.ozet_hesapla(s), "sonuclar": s}
        self.assertIn("Başarı: 1/1", o.rapor_yaz(v, None))


if __name__ == "__main__":
    unittest.main()
