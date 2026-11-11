"""Olcumde gorulen ajan hatalari: her biri once yeniden uretilir, sonra duzeltme dogrulanir."""
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a


def yanit(icerik="", **cagri):
    cagrilar = [{"function": {"name": ad, "arguments": arg}} for ad, arg in cagri.items()]
    return {"role": "assistant", "content": icerik, "tool_calls": cagrilar}


class Arayuz(a.TerminalArayuz):
    def __init__(self):
        self.hep_izin = True
        self.uyarilar, self.hatalar = [], []

    def uyari(self, m):
        self.uyarilar.append(m)

    def hata(self, m):
        self.hatalar.append(m)

    def arac(self, ad, arg):
        pass

    def sonuc(self, ad, m):
        pass

    def degisiklik(self, *x):
        pass

    def sor(self, soru):
        return "e"


class AraNotTesti(unittest.TestCase):
    """Model arac cagirmadan once Ingilizce not yaziyor ve Ollama bunu metin olarak gonderiyor (panelde goruldu)."""

    def setUp(self):
        g = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, g, ignore_errors=True)
        ortam = patch.dict(os.environ, {"KOD_AJANI_VERI": str(g / "v")})
        ortam.start()
        self.addCleanup(ortam.stop)
        (g / "p").mkdir()
        self.olaylar = []
        olaylar = self.olaylar

        class Ar(a.JsonArayuz):
            def yaz(self, tur, **v):
                olaylar.append(tur)
        self.ajan = a.Ajan(g / "p", "sahte", arayuz=Ar())
        self.ajan.dusun = False

    def akis(self, *parcalar):
        return patch.object(a, "model_akisi", lambda *x, **y: iter(parcalar))

    def test_arac_oncesi_metin_ara_not_sayilir(self):
        with self.akis({"message": {"content": "Let's list."}},
                       {"message": {"tool_calls": [{"function": {"name": "list_files", "arguments": {}}}]}, "done": True}):
            self.ajan._modeli_cagir()
        self.assertEqual(self.olaylar, ["icerik", "ara_not", "mesaj_bitti"])

    def test_son_cevap_ara_not_degildir(self):
        with self.akis({"message": {"content": "Projede yalniz GOREV.md var."}, "done": True}):
            self.ajan._modeli_cagir()
        self.assertNotIn("ara_not", self.olaylar)

    def test_metinsiz_arac_cagrisi(self):
        with self.akis({"message": {"tool_calls": [{"function": {"name": "list_files", "arguments": {}}}]}, "done": True}):
            self.ajan._modeli_cagir()
        self.assertNotIn("ara_not", self.olaylar)


class ModelTesti(unittest.TestCase):
    def setUp(self):
        self.g = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.g, ignore_errors=True)
        ortam = patch.dict(os.environ, {"KOD_AJANI_VERI": str(self.g / "v")})
        ortam.start()
        self.addCleanup(ortam.stop)
        self.kok = self.g / "p"
        self.kok.mkdir()
        (self.kok / "a.py").write_text("x = 1\n", encoding="utf-8")
        self.ajan = a.Ajan(self.kok, "sahte", arayuz=Arayuz())

    def kurgula(self, *yanitlar):
        sira = iter(yanitlar)

        def model():
            y = next(sira)
            if isinstance(y, Exception):
                raise y
            return y
        self.ajan._modeli_cagir = model

    def test_bozuk_arac_cagrisi_yeniden_denenir(self):
        self.kurgula(a.ModelHatasi("error parsing tool call: raw='We need'"), yanit("bitti", read_file={"path": "a.py"}), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertTrue([m for m in self.ajan.mesajlar if m["content"] == a.BOZUK_CAGRI_NOTU])

    def test_bozuk_cagri_siniri_var_tur_temizlenir(self):
        h = a.ModelHatasi("error parsing tool call")
        once = len(self.ajan.mesajlar)
        self.kurgula(h, h, h, yanit("asla"))
        self.assertFalse(self.ajan.tur("isle"))
        self.assertEqual(len(self.ajan.mesajlar), once)
        self.assertTrue(self.ajan.arayuz.hatalar)

    def test_baska_model_hatasi_yeniden_denenmez(self):
        cagri = {"n": 0}

        def model():
            cagri["n"] += 1
            raise a.ModelHatasi("Ollama'ya ulasilamadi")
        self.ajan._modeli_cagir = model
        self.assertFalse(self.ajan.tur("isle"))
        self.assertEqual(cagri["n"], 1)

    def test_bos_yanitta_devam_ettirilir(self):
        self.kurgula(yanit(read_file={"path": "a.py"}), yanit(""), yanit("oldu"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertTrue([m for m in self.ajan.mesajlar if m["content"] == a.BOS_YANIT_NOTU])

    @patch.dict(os.environ, {"AIRGAP_LANG": "en"})  # checks the English UI text
    def test_bos_yanit_siniri_var(self):
        self.kurgula(yanit(), yanit(), yanit(), yanit("asla"))
        self.assertFalse(self.ajan.tur("isle"))
        self.assertIn("empty reply", self.ajan.arayuz.hatalar[-1])


class TekrarVeDogrulamaTesti(ModelTesti):
    def test_tekrar_once_uyarir_sonra_durur(self):
        c = {"read_file": {"path": "a.py"}}
        self.kurgula(*[yanit(**c) for _ in range(6)])
        self.assertFalse(self.ajan.tur("isle"))
        notlar = [m for m in self.ajan.mesajlar if m.get("content") == a.TEKRAR_NOTU]
        self.assertEqual(len(notlar), 2)

    def test_uyaridan_sonra_farkli_yol_devam_eder(self):
        c = {"read_file": {"path": "a.py"}}
        self.kurgula(yanit(**c), yanit(**c), yanit(**c), yanit(list_files={}), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))

    def test_ayni_hata_ucuncu_kezde_not_besinci_kezde_durur(self):
        h = {"edit_file": {"path": "a.py", "old_text": "yok", "new_text": "q"}}
        o = {"read_file": {"path": "a.py"}}
        self.kurgula(*[y for _ in range(6) for y in (yanit(**h), yanit(**o))])
        self.assertFalse(self.ajan.tur("isle"))
        self.assertEqual(len([m for m in self.ajan.mesajlar if m.get("content") == a.HATA_TEKRAR_NOTU]), 1)

    def duzenleme_akisi(self, *son):
        d = {"edit_file": {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}}
        self.kurgula(yanit(**d), *son)

    def test_otomatik_dogrulama_basarisizsa_modele_doner(self):
        (self.kok / "test_a.py").write_text("x\n", encoding="utf-8")
        self.ajan.araclar.kum = object()
        sonuclar = iter(["FAIL\n[cikis kodu: 1]", "OK\n[cikis kodu: 0]"])
        self.ajan._calistir_ve_bildir = lambda ad, arg: next(sonuclar) if ad == "run_command" else "duzenlendi"
        self.duzenleme_akisi(yanit("bitti"), yanit("gercekten bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual(len([m for m in self.ajan.mesajlar if "[Automatic check]" in (m.get("content") or "")]), 1)
        self.assertEqual(self.ajan.mesajlar[-1]["content"], "gercekten bitti")

    def test_dogrulama_sinirli(self):
        (self.kok / "test_a.py").write_text("x\n", encoding="utf-8")
        self.ajan.araclar.kum = object()
        self.ajan._calistir_ve_bildir = lambda ad, arg: "FAIL\n[cikis kodu: 1]" if ad == "run_command" else "duzenlendi"
        self.duzenleme_akisi(yanit("bitti"), yanit("bitti"), yanit("bitti"), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual(len([m for m in self.ajan.mesajlar if "[Automatic check]" in (m.get("content") or "")]), 2)

    def test_koruma_veya_izin_yoksa_sormadan_komut_calismaz(self):
        (self.kok / "test_a.py").write_text("x\n", encoding="utf-8")
        calisan = []
        self.ajan._calistir_ve_bildir = lambda ad, arg: calisan.append(ad) or "duzenlendi"
        self.ajan.arayuz.sor = lambda s: "e"
        self.duzenleme_akisi(yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertNotIn("run_command", calisan)

    def test_test_yoksa_dogrulama_yok(self):
        self.ajan.araclar.kum = object()
        calisan = []
        self.ajan._calistir_ve_bildir = lambda ad, arg: calisan.append(ad) or "duzenlendi"
        self.duzenleme_akisi(yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertNotIn("run_command", calisan)

    def test_duzenleme_yoksa_dogrulama_yok(self):
        (self.kok / "test_a.py").write_text("x\n", encoding="utf-8")
        self.ajan.araclar.kum = object()
        self.kurgula(yanit(read_file={"path": "a.py"}), yanit("cevap"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertFalse([m for m in self.ajan.mesajlar if "[Automatic check]" in (m.get("content") or "")])


class BitirmeTesti(ModelTesti):
    def test_yarim_cagri_taninir(self):
        for m in ['{"line_end":690,"line_start":668,"path":"src/click/types.py"}',
                  'Inspect it.{"path":"src/click/core.py","pattern":"class Option("}',
                  '```json\n{"query": "slug"}\n```']:
            self.assertTrue(a.yarim_arac_cagrisi(m), m)
        for m in ["Bitti.", 'Ayar: {"timeout": 5}', '{"bozuk": ', '{}', 'Dosya {"path": "a"} sonra devam']:
            self.assertFalse(a.yarim_arac_cagrisi(m), m)

    def test_yarim_cagri_son_yanit_sayilmaz(self):
        self.kurgula(yanit('{"path":"a.py"}'), yanit(read_file={"path": "a.py"}), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual(self.ajan.mesajlar[-1]["content"], "bitti")
        self.assertFalse([m for m in self.ajan.mesajlar if m.get("role") == "assistant" and '{"path":"a.py"}' == m.get("content")])

    def test_yarim_cagri_siniri_var(self):
        self.kurgula(yanit('{"path":"a.py"}'), yanit('{"path":"a.py"}'), yanit('{"path":"a.py"}'), yanit("son"))
        self.assertTrue(self.ajan.tur("isle"))

    def test_uygulanmayan_kod_bir_kez_hatirlatilir(self):
        d = {"edit_file": {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}}
        self.kurgula(yanit(read_file={"path": "a.py"}), yanit("Şöyle yap:\n```python\nx = 2\n```"), yanit(**d), yanit("uygulandi"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual((self.kok / "a.py").read_text(encoding="utf-8"), "x = 2\n")

    def test_soruya_kodlu_yanit_ikinci_kez_kabul_edilir(self):
        k = "Cevap:\n```python\nx = 1\n```"
        self.kurgula(yanit(read_file={"path": "a.py"}), yanit(k), yanit(k))
        self.assertTrue(self.ajan.tur("nedir"))
        self.assertEqual(self.ajan.mesajlar[-1]["content"], k)

    def test_duzenleme_sonrasi_kod_hatirlatmasi_yok(self):
        d = {"edit_file": {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}}
        self.kurgula(yanit(**d), yanit("Yaptım:\n```\nx = 2\n```"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertFalse([m for m in self.ajan.mesajlar if m.get("content") == a.KOD_UYGULANMADI_NOTU])

    def test_adim_butcesi_uyarilari(self):
        self.ajan.maks_adim = 10
        d = {"edit_file": {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}}
        oku = [yanit(list_files={"path": f"./{'.' * 0}"}) if i % 2 else yanit(read_file={"path": "a.py", "offset": i + 1}) for i in range(12)]
        self.kurgula(yanit(**d), *oku)
        self.assertFalse(self.ajan.tur("isle"))
        self.assertEqual(len([m for m in self.ajan.mesajlar if "steps" in (m.get("content") or "") and "You have used" in m["content"]]), 1)
        self.assertEqual(len([m for m in self.ajan.mesajlar if "Only 3 steps" in (m.get("content") or "")]), 1)

    def test_duzenleme_yoksa_butce_notu_yok(self):
        self.ajan.maks_adim = 10
        oku = [yanit(read_file={"path": "a.py", "offset": i + 1}) for i in range(12)]
        self.kurgula(*oku)
        self.ajan.tur("isle")
        self.assertFalse([m for m in self.ajan.mesajlar if "You have used" in (m.get("content") or "")])


class BaglamTesti(unittest.TestCase):
    def test_eski_buyuk_duzenleme_kisalir_son_mesajlara_dokunulmaz(self):
        buyuk = "x" * 5000
        mesajlar = [{"role": "assistant", "content": "", "tool_calls": [
            {"function": {"name": "write_file", "arguments": {"path": "a.py", "content": buyuk}}}]} for _ in range(10)]
        a.gecmisi_sigdir(mesajlar, 1000)
        self.assertLess(len(mesajlar[0]["tool_calls"][0]["function"]["arguments"]["content"]), 200)
        self.assertEqual(mesajlar[0]["tool_calls"][0]["function"]["arguments"]["path"], "a.py")
        self.assertEqual(len(mesajlar[-1]["tool_calls"][0]["function"]["arguments"]["content"]), 5000)

    def test_butce_icinde_dokunulmaz(self):
        m = [{"role": "tool", "tool_name": "x", "content": "y" * 500} for _ in range(10)]
        a.gecmisi_sigdir(m, 100000)
        self.assertEqual(len(m[0]["content"]), 500)


class SozdizimiTesti(unittest.TestCase):
    def setUp(self):
        self.g = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.g, ignore_errors=True)
        self.a = a.Araclar(self.g)

    def yaz(self, ad, m):
        (self.g / ad).write_bytes(m.encode("utf-8"))

    def test_girintiyi_bozan_duzenleme_uygulanmaz(self):
        self.yaz("a.py", "def f():\n    return 1\n")
        s = self.a.calistir("edit_file", {"path": "a.py", "old_text": "    return 1", "new_text": "      x = 1\n    return x"})
        self.assertTrue(s.startswith("HATA"), s)
        self.assertIn("sozdizimi", s)
        self.assertIn("satir", s)
        self.assertEqual((self.g / "a.py").read_text(), "def f():\n    return 1\n")

    def test_dosya_yazma_da_denetlenir(self):
        self.yaz("a.py", "x = 1\n")
        self.assertTrue(self.a.calistir("write_file", {"path": "a.py", "content": "def (:\n"}).startswith("HATA"))
        self.assertTrue(self.a.calistir("write_file", {"path": "yeni.py", "content": "def (:\n"}).startswith("HATA"))
        self.assertFalse((self.g / "yeni.py").exists())

    def test_gecerli_duzenleme_gecer(self):
        self.yaz("a.py", "x = 1\n")
        self.assertIn("duzenlendi", self.a.calistir("edit_file", {"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}))

    def test_zaten_bozuk_dosya_duzeltilebilir(self):
        self.yaz("a.py", "def f(\n")
        self.assertIn("duzenlendi", self.a.calistir("edit_file", {"path": "a.py", "old_text": "def f(", "new_text": "def f(:"}))

    def test_python_disi_dosya_denetlenmez(self):
        self.yaz("a.txt", "x\n")
        self.assertIn("duzenlendi", self.a.calistir("edit_file", {"path": "a.txt", "old_text": "x", "new_text": "def (:"}))

    def test_ayni_metin_yol_gosterir(self):
        self.yaz("a.py", "x = 1\n")
        s = self.a.calistir("edit_file", {"path": "a.py", "old_text": "x = 1", "new_text": "x = 1"})
        self.assertIn("new_text degistirilmis kodu icermeli", s)


if __name__ == "__main__":
    unittest.main()
