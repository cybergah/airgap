import os
import tempfile
import unittest
from unittest.mock import patch
from unittest import mock
from pathlib import Path

import ajan as a


class AracTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.kok = Path(self.gecici.name)
        self.araclar = a.Araclar(self.kok)

    def tearDown(self):
        self.gecici.cleanup()

    def test_proje_disina_cikilamaz(self):
        for yol in ("../disari.txt", str(self.kok.parent / "disari.txt")):
            sonuc = self.araclar.calistir("write_file", {"path": yol, "content": "x"})
            self.assertTrue(sonuc.startswith("HATA"), sonuc)
        self.assertFalse((self.kok.parent / "disari.txt").exists())

    def test_yazma_ve_okuma(self):
        self.araclar.calistir("write_file", {"path": "alt/a.txt", "content": "bir\niki\nuc\n"})
        self.assertEqual(self.araclar.calistir("read_file", {"path": "alt/a.txt", "offset": 2, "limit": 1}),
                         "2\tiki")

    def test_duzenleme_benzersiz_olmali(self):
        (self.kok / "a.txt").write_text("x\nx\n")
        sonuc = self.araclar.calistir("edit_file", {"path": "a.txt", "old_text": "x", "new_text": "y"})
        self.assertIn("2 kez", sonuc)
        self.assertEqual((self.kok / "a.txt").read_text(), "x\nx\n")

    def test_bos_duzenleme_reddedilir(self):
        (self.kok / "a.txt").write_text("x\n")
        sonuc = self.araclar.calistir("edit_file", {"path": "a.txt", "old_text": "x", "new_text": "x"})
        self.assertIn("ayni", sonuc)

    def test_duzenleme_crlf_korur(self):
        (self.kok / "a.txt").write_bytes(b"bir\r\niki\r\nuc\r\n")
        self.araclar.calistir("edit_file", {"path": "a.txt", "old_text": "bir\niki", "new_text": "1\n2"})
        self.assertEqual((self.kok / "a.txt").read_bytes(), b"1\r\n2\r\nuc\r\n")

    def test_duzenleme_satir_numarasini_tolere_eder(self):
        (self.kok / "a.py").write_text("def f():\n    return 1\n")
        sonuc = self.araclar.calistir("edit_file", {
            "path": "a.py", "old_text": "2\t    return 1", "new_text": "2\t    return 2"})
        self.assertIn("duzenlendi", sonuc)
        self.assertEqual((self.kok / "a.py").read_text(), "def f():\n    return 2\n")

    def test_duzenleme_girinti_farkini_tolere_eder(self):
        (self.kok / "a.py").write_text("def f():\n    if x:\n        return 1\n")
        sonuc = self.araclar.calistir("edit_file", {
            "path": "a.py", "old_text": "if x:\n    return 1", "new_text": "if y:\n    return 2"})
        self.assertIn("duzenlendi", sonuc)
        self.assertEqual((self.kok / "a.py").read_text(), "def f():\n    if y:\n        return 2\n")

    def test_esnek_eslesme_birden_cok_yerde_tahmin_yapmaz(self):
        icerik = "    a = 1\nb\n        a = 1\n"
        (self.kok / "a.py").write_text(icerik)
        sonuc = self.araclar.calistir("edit_file", {
            "path": "a.py", "old_text": "  a = 1", "new_text": "  a = 2"})
        self.assertTrue(sonuc.startswith("HATA"), sonuc)
        self.assertEqual((self.kok / "a.py").read_text(), icerik)

    def test_bulunamayan_metin_en_yakin_satiri_gosterir(self):
        (self.kok / "a.py").write_text("return sum(x for x in y)\n")
        sonuc = self.araclar.calistir("edit_file", {
            "path": "a.py", "old_text": "return sum(z for x in y)", "new_text": "q"})
        self.assertIn("return sum(x for x in y)", sonuc)

    def test_diff_bicimi_ne_yapilacagini_soyler(self):
        (self.kok / "a.py").write_text("def f():\n    return 1\n")
        fark = "def f():\n-    return 1"
        for yeni in (fark, "def f():\n+    return 2"):
            sonuc = self.araclar.calistir("edit_file", {"path": "a.py", "old_text": fark, "new_text": yeni})
            self.assertTrue(sonuc.startswith("HATA"), sonuc)
            self.assertIn("Do not write a diff", sonuc)
            self.assertIn("write_file", sonuc)
        self.assertEqual((self.kok / "a.py").read_text(), "def f():\n    return 1\n")

    def test_diff_olmayan_hatada_ipucu_yoktur(self):
        (self.kok / "a.py").write_text("x = 1\n")
        sonuc = self.araclar.calistir("edit_file", {"path": "a.py", "old_text": "y = 2", "new_text": "y = 3"})
        self.assertNotIn("Do not write a diff", sonuc)

    def test_arama_atlanan_klasorleri_gormez(self):
        (self.kok / "node_modules").mkdir()
        (self.kok / "node_modules" / "b.js").write_text("hedef")
        (self.kok / "a.js").write_text("hedef")
        self.assertEqual(self.araclar.calistir("search_text", {"pattern": "hedef"}), "a.js:1:hedef")

    def test_komut_cikis_kodunu_dondurur(self):
        sonuc = self.araclar.calistir("run_command", {"command": "python -c \"print('merhaba'); exit(3)\""})
        self.assertIn("merhaba", sonuc)
        self.assertIn("cikis kodu: 3", sonuc)

    def test_eksik_arguman_hata_olur(self):
        self.assertIn("gecersiz arguman", self.araclar.calistir("read_file", {}))


class AyristirmaTesti(unittest.TestCase):
    def test_etiketli_cagri(self):
        c = a.metinden_arac_cagrilari(
            'Bakiyorum <tool_call>{"name": "read_file", "arguments": {"path": "a"}}</tool_call>')
        self.assertEqual(c[0]["function"]["name"], "read_file")

    def test_deepseek_belirteci(self):
        c = a.metinden_arac_cagrilari(
            '<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>function<｜tool▁sep｜>read_file\n'
            '```json\n{"path": "a"}\n```<｜tool▁call▁end｜><｜tool▁calls▁end｜>')
        self.assertEqual(c[0]["function"]["arguments"], {"path": "a"})

    def test_tam_mesaj_json(self):
        c = a.metinden_arac_cagrilari('```json\n{"name": "list_files", "arguments": {}}\n```')
        self.assertEqual(c[0]["function"]["name"], "list_files")

    def test_aciklamadaki_ornek_calismaz(self):
        metin = 'Ornek:\n```json\n{"name": "run_command", "arguments": {"command": "rm -rf x"}}\n```\nbu kadar'
        self.assertEqual(a.metinden_arac_cagrilari(metin), [])

    def test_bilinmeyen_arac_calismaz(self):
        self.assertEqual(a.metinden_arac_cagrilari('{"name": "sil", "arguments": {}}'), [])


class DonguTesti(unittest.TestCase):
    def _ajan(self, kok):
        ajan = a.Ajan(Path(kok), "sahte")
        ajan._modeli_cagir = lambda: {
            "role": "assistant", "content": "",
            "tool_calls": [{"function": {"name": "run_command", "arguments": {"command": "x"}}}]}
        return ajan

    def test_gecersiz_onay_yaniti_yeniden_sorulur(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as kok:
            ajan = a.Ajan(Path(kok), "sahte")
            with patch("builtins.input", side_effect=["ee", "", "e"]) as girdi:
                self.assertTrue(ajan._onay("Soru?"))
            self.assertEqual(girdi.call_count, 3)
            with patch("builtins.input", side_effect=["h"]):
                self.assertFalse(ajan._onay("Soru?"))

    def test_reddedilen_islem_yeniden_sorulmaz(self):
        with tempfile.TemporaryDirectory() as kok:
            ajan = self._ajan(kok)
            sorular = []
            ajan._onay = lambda soru, tur="yazma": sorular.append(soru) or False
            self.assertFalse(ajan.tur("calistir"))
            self.assertEqual(len(sorular), 1)
            self.assertEqual(ajan.mesajlar[-1]["role"], "tool")

    def test_reddedilen_islem_icin_bir_uyari_hakki_vardir(self):
        with tempfile.TemporaryDirectory() as kok:
            ajan = self._ajan(kok)
            ajan._onay = lambda soru, tur="yazma": False
            self.assertFalse(ajan.tur("calistir"))
            arac = [m["content"] for m in ajan.mesajlar if m["role"] == "tool"]
            self.assertEqual(arac, [a.REDDEDILDI, a.YENIDEN_ISTENDI, arac[-1]])
            self.assertIn("Stopped", arac[-1])

    def test_ayni_hatali_cagri_uc_kez_denenince_durur(self):
        with tempfile.TemporaryDirectory() as kok:
            (Path(kok) / "a.py").write_text("x\n")
            ajan = a.Ajan(Path(kok), "sahte")
            cagrilar = iter([("edit_file", {"path": "a.py", "old_text": "yok", "new_text": "q"}),
                             ("read_file", {"path": "a.py"})] * 5)

            def model():
                ad, arg = next(cagrilar)
                return {"role": "assistant", "content": "",
                        "tool_calls": [{"function": {"name": ad, "arguments": arg}}]}

            ajan._modeli_cagir = model
            self.assertFalse(ajan.tur("duzenle"))
            hata = [m for m in ajan.mesajlar if m["role"] == "tool" and m["content"].startswith("ERROR")]
            self.assertEqual(len(hata), a.TEKRAR_SINIRI)

    def test_uyaridan_sonra_farkli_islem_devam_eder(self):
        with tempfile.TemporaryDirectory() as kok:
            ajan = a.Ajan(Path(kok), "sahte")
            yanitlar = iter([
                ("run_command", {"command": "x"}), ("run_command", {"command": "x"}),
                ("run_command", {"command": "y"}), None])

            def model():
                y = next(yanitlar)
                if y is None:
                    return {"role": "assistant", "content": "bitti", "tool_calls": []}
                return {"role": "assistant", "content": "",
                        "tool_calls": [{"function": {"name": y[0], "arguments": y[1]}}]}

            ajan._modeli_cagir = model
            onaylar = iter([False, True])
            ajan._onay = lambda soru, tur="yazma": next(onaylar)
            ajan.araclar.calistir = lambda ad, arg: "tamam"
            self.assertTrue(ajan.tur("calistir"))

    def test_ayni_cagri_tekrarlaninca_durur(self):
        with tempfile.TemporaryDirectory() as kok:
            ajan = self._ajan(kok)
            ajan._onay = lambda soru, tur="yazma": True
            calisan = []
            ajan.araclar.calistir = lambda ad, arg: calisan.append(ad) or "tamam"
            self.assertFalse(ajan.tur("calistir"))
            self.assertEqual(len(calisan), 2)


class AdresTesti(unittest.TestCase):
    def test_adresler(self):
        for deger, beklenen in [
            (None, "http://127.0.0.1:11434"),
            ("0.0.0.0", "http://127.0.0.1:11434"),
            ("0.0.0.0:1234", "http://127.0.0.1:1234"),
            (":11434", "http://127.0.0.1:11434"),
            ("http://0.0.0.0:11434/", "http://127.0.0.1:11434"),
            ("sunucu:8080", "http://sunucu:8080"),
            ("https://ornek.com", "https://ornek.com:443"),
        ]:
            self.assertEqual(a.ollama_adresi(deger), beklenen, deger)


class GecmisTesti(unittest.TestCase):
    def test_eski_arac_ciktisi_kisalir_son_mesajlar_kalir(self):
        mesajlar = [{"role": "tool", "tool_name": "x", "content": "a" * 5000} for _ in range(10)]
        a.gecmisi_sigdir(mesajlar, 1000)
        self.assertLess(len(mesajlar[0]["content"]), 300)
        self.assertEqual(len(mesajlar[-1]["content"]), 5000)

    def test_kirpma_tek_seferde_bol_yapilir_sonra_dokunulmaz(self):
        """Onbellek icin: butce asilinca gecmis butcenin %60'ina iner, sonraki birkac adimda basi hic degismez."""
        mesajlar = [{"role": "tool", "tool_name": "x", "content": "a" * 1000} for _ in range(30)]
        a.gecmisi_sigdir(mesajlar, 0, 20000)
        self.assertLessEqual(a.mesajlar_boyutu(mesajlar), 20000 * a.KIRPMA_ORANI)
        bas = [m["content"] for m in mesajlar]
        for _ in range(5):  # her adim ~1000 harf ekler; butceye daha var
            mesajlar.append({"role": "tool", "tool_name": "x", "content": "b" * 1000})
            a.gecmisi_sigdir(mesajlar, 0, 20000)
        self.assertEqual([m["content"] for m in mesajlar[:30]], bas, "gecmisin basi degismedi")

    def test_butce_asilmadikca_dusunce_bile_silinmez(self):
        mesajlar = [{"role": "assistant", "content": "", "thinking": "d" * 500}, {"role": "tool", "content": "x"}]
        a.gecmisi_sigdir(mesajlar, 0, 1000)
        self.assertEqual(mesajlar[0]["thinking"], "d" * 500)

    def test_eski_kirpma_orani_secilebilir(self):
        mesajlar = [{"role": "tool", "tool_name": "x", "content": "a" * 1000} for _ in range(30)]
        with patch.object(a, "KIRPMA_ORANI", 1.0):
            a.gecmisi_sigdir(mesajlar, 0, 20000)
        self.assertGreater(a.mesajlar_boyutu(mesajlar), 20000 * 0.9)

    def test_harf_orani_gercek_belirtecten_ogrenilir(self):
        self.assertAlmostEqual(a.harf_orani(30000, 15000, 3.0), 2.0)
        self.assertEqual(a.harf_orani(30000, 300, 3.0), 3.0)  # onbellekten okunan cagri: yalniz yeni kisim sayildi
        self.assertEqual(a.harf_orani(30000, 9000, 2.0), 2.0)  # daha iyi oran gorulse de en kotusu kalir
        self.assertEqual(a.harf_orani(30000, 29000, 3.0), a.EN_DUSUK_HARF_ORANI)

    def test_butce_cevaba_yer_birakir_ve_orana_uyar(self):
        tam = 16384 * 3
        self.assertLess(a.sigdirma_butcesi(16384), tam * 0.8)
        self.assertLess(a.sigdirma_butcesi(16384, 2.0), a.sigdirma_butcesi(16384, 3.0))

    def test_dusuk_oranda_daha_cok_kisaltilir(self):
        def yap():
            return [{"role": "tool", "tool_name": "x", "content": "a" * 1000} for _ in range(60)]
        genis, dar = yap(), yap()
        a.gecmisi_sigdir(genis, 16384, a.sigdirma_butcesi(16384, 3.0))
        a.gecmisi_sigdir(dar, 16384, a.sigdirma_butcesi(16384, 2.0))
        self.assertLess(a.mesajlar_boyutu(dar), a.mesajlar_boyutu(genis))


class OrneklemeTesti(unittest.TestCase):
    def test_qwen_onerilen_ayarlari_alir_digerleri_eski(self):
        self.assertEqual(a.ornekleme_ayarlari("qwen3.6:35b-a3b")["temperature"], 0.6)
        self.assertEqual(a.ornekleme_ayarlari("qwen3.6:35b-a3b")["presence_penalty"], 0.0)
        self.assertEqual(a.ornekleme_ayarlari("gpt-oss:20b"), {"temperature": 0.2})
        self.assertEqual(a.ornekleme_ayarlari("qwen2.5:14b"), {"temperature": 0.2})


class ModelDiliTesti(unittest.TestCase):
    """Arac sonuclari modele arayuz dilinden bagimsiz Ingilizce gider; dosya icerigi ve komut ciktisi aynen."""

    def test_sonuc_ve_hata_ingilizce(self):
        self.assertEqual(a.model_sonucu("cart.py duzenlendi"), "cart.py edited")
        self.assertEqual(a.model_sonucu("Ran 3 tests\n\nOK\n[cikis kodu: 0]"), "Ran 3 tests\n\nOK\n[exit code: 0]")
        self.assertEqual(a.model_sonucu("HATA: gecersiz arguman: x"), "ERROR: invalid argument: x")
        self.assertIn("must be a string", a.model_sonucu("HATA: content metin (string) olmali, dict geldi. "
                                                         "JSON icerigi de tek bir metin olarak yaz."))

    def test_dosya_icerigi_cevrilmez(self):
        icerik = "1\tprint('dosya bulunamadi: x')"
        self.assertEqual(a.model_sonucu(icerik), icerik)

    def test_turkce_arayuzde_de_model_ingilizce_gorur(self):
        with mock.patch.dict(os.environ, {"AIRGAP_LANG": "tr"}), tempfile.TemporaryDirectory() as kok:
            (Path(kok) / "a.py").write_text("x = 1\n")
            ajan = a.Ajan(Path(kok), "sahte")
            cagrilar = iter([("edit_file", {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"})])

            def model():
                try:
                    ad, arg = next(cagrilar)
                except StopIteration:
                    return {"role": "assistant", "content": "done", "tool_calls": []}
                return {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": ad, "arguments": arg}}]}

            ajan._modeli_cagir = model
            ajan._onay = lambda soru, tur="yazma": True
            ajan.tur("duzenle")
            arac = [m["content"] for m in ajan.mesajlar if m["role"] == "tool"]
            self.assertEqual(arac[0], "a.py edited")

    def test_read_file_line_takma_adi(self):
        with tempfile.TemporaryDirectory() as kok:
            (Path(kok) / "a.py").write_text("bir\niki\nuc\n")
            self.assertEqual(a.Araclar(Path(kok)).read_file("a.py", line=2), "2\tiki\n3\tuc")


if __name__ == "__main__":
    unittest.main()
