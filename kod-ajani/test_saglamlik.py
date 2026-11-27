"""Olcumde gorulen ajan hatalari: her biri once yeniden uretilir, sonra duzeltme dogrulanir."""
import os
import shutil
import sys
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
        self.assertEqual(self.ajan.silinen_tur[0], {"role": "user", "content": "isle"}, "silinen tur kayit icin saklanir")
        self.assertIn(a.BOZUK_CAGRI_NOTU, [m["content"] for m in self.ajan.silinen_tur])
        self.kurgula(*[yanit("tamam")] * 3)
        self.assertTrue(self.ajan.tur("yeni"))
        self.assertEqual(self.ajan.silinen_tur, [], "sonraki turda sifirlanir")

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
        self.ajan._sessiz_komut = lambda komut: "OK\n[cikis kodu: 0]"  # duzenlemeden once testler geciyordu
        self.ajan._calistir_ve_bildir = lambda ad, arg: next(sonuclar) if ad == "run_command" else "duzenlendi"
        self.duzenleme_akisi(yanit("bitti"), yanit("gercekten bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertEqual(len([m for m in self.ajan.mesajlar if "[Automatic check]" in (m.get("content") or "")]), 1)
        self.assertEqual(self.ajan.mesajlar[-1]["content"], "gercekten bitti")

    def test_dogrulama_sinirli(self):
        (self.kok / "test_a.py").write_text("x\n", encoding="utf-8")
        self.ajan.araclar.kum = object()
        self.ajan._calistir_ve_bildir = lambda ad, arg: "FAIL\n[cikis kodu: 1]" if ad == "run_command" else "duzenlendi"
        self.ajan._sessiz_komut = lambda komut: "OK\n[cikis kodu: 0]"
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


    def anlik_kur(self, *kosular):
        """Testli proje, korumali ortam; ilk _sessiz_komut taban, sonrakiler duzenleme sonrasi kosular."""
        (self.kok / "test_a.py").write_text("x\n", encoding="utf-8")
        self.ajan.araclar.kum = object()
        sira = iter(["OK\n[cikis kodu: 0]", *kosular])
        self.kosulan = []
        self.ajan._sessiz_komut = lambda komut: self.kosulan.append(komut) or next(sira)
        self.ajan._calistir_ve_bildir = lambda ad, arg: "OK\n[cikis kodu: 0]" if ad == "run_command" else "duzenlendi"

    def duzenleme_sonucu(self):
        return next(m["content"] for m in self.ajan.mesajlar if m["role"] == "tool" and m.get("tool_name") == "edit_file")

    def test_anlik_kontrol_bozulan_testi_bilgi_notu_olarak_ekler(self):
        self.anlik_kur("FAIL: test_x (test_a.T.test_x)\nFAILED (failures=1)\n[cikis kodu: 1]")
        self.duzenleme_akisi(yanit("bitti"))
        self.ajan.tur("isle")
        sonuc = self.duzenleme_sonucu()
        self.assertTrue(sonuc.startswith("duzenlendi\n\n[Note]"), sonuc)
        self.assertIn("- test_a.T.test_x", sonuc)
        self.assertNotIn("(failures=1)\n-", sonuc)
        self.assertIn("can be expected", sonuc)
        self.assertEqual(self.ajan.anlik_izleri[0]["yeni"], 1)

    def test_anlik_kontrol_gecerse_kisa_not(self):
        self.anlik_kur("OK\n[cikis kodu: 0]")
        self.duzenleme_akisi(yanit("bitti"))
        self.ajan.tur("isle")
        self.assertIn("nothing that passed before fails now", self.duzenleme_sonucu())

    def test_anlik_kontrol_python_disi_dosyada_calismaz(self):
        self.anlik_kur()
        (self.kok / "README.md").write_text("x = 1\n", encoding="utf-8")
        self.kurgula(yanit(edit_file={"path": "README.md", "old_text": "x = 1", "new_text": "x = 2"}), yanit("bitti"))
        self.ajan.tur("isle")
        self.assertEqual(self.duzenleme_sonucu(), "duzenlendi")
        self.assertEqual(len(self.kosulan), 1, "yalniz taban kosusu")

    def test_anlik_kontrol_testsiz_veya_kapaliyken_calismaz(self):
        calisan = []
        self.ajan.araclar.kum = object()
        self.ajan._sessiz_komut = lambda komut: calisan.append(komut) or "OK\n[cikis kodu: 0]"
        self.ajan._calistir_ve_bildir = lambda ad, arg: "duzenlendi"
        self.duzenleme_akisi(yanit("bitti"))
        self.ajan.tur("isle")
        self.assertEqual((calisan, self.duzenleme_sonucu()), ([], "duzenlendi"), "test dosyasi yok")
        self.anlik_kur("FAIL: test_x (test_a.T.test_x)\n[cikis kodu: 1]")
        with patch.object(a, "ANLIK_KONTROL", False):
            self.ajan.mesajlar = self.ajan.mesajlar[:1]
            self.ajan._test_taban = None
            self.duzenleme_akisi(yanit("bitti"))
            self.ajan.tur("isle")
        self.assertEqual(self.duzenleme_sonucu(), "duzenlendi")

    def test_anlik_kontrol_yavassa_turda_kapanir(self):
        self.anlik_kur("OK\n[cikis kodu: 0]")
        zaman = iter([0, 0, 0, a.TEST_SURE_SINIRI + 1])  # taban hizli, ilk anlik kosu yavas
        with patch.object(a.time, "monotonic", lambda: next(zaman, 10_000)):
            self.kurgula(yanit(edit_file={"path": "a.py", "old_text": "x = 1", "new_text": "x = 2"}),
                         yanit(edit_file={"path": "a.py", "old_text": "x = 2", "new_text": "x = 3"}), yanit("bitti"))
            self.ajan.tur("isle")
        self.assertEqual(self.ajan.anlik_izleri, [{"sure": a.TEST_SURE_SINIRI + 1, "yeni": None}])
        self.assertEqual(len(self.kosulan), 2, "yavas kosudan sonra bir daha calismaz")


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


class DusunmeSeviyesiTesti(ModelTesti):
    def test_think_degeri(self):
        self.ajan.dusun = True
        self.assertIs(self.ajan._think(), True, "seviye yoksa modelin varsayilani")
        for s in a.DUSUNME_SEVIYELERI:
            self.ajan.dusunme_seviyesi = s
            self.assertEqual(self.ajan._think(), s)
        self.ajan.dusunme_seviyesi = "cok"
        self.assertIs(self.ajan._think(), True, "gecersiz seviye yok sayilir")
        self.ajan.dusun = False
        self.ajan.dusunme_seviyesi = "low"
        self.assertIs(self.ajan._think(), False, "dusunme desteklenmiyorsa hic gonderilmez")

    def test_model_cagrisina_gider(self):
        self.ajan.dusun, self.ajan.dusunme_seviyesi = True, "low"
        gelen = {}

        def akis(model, mesajlar, baglam, dusun=False, araclar=True):
            gelen["think"] = dusun
            yield {"message": {"content": "tamam"}, "done": True}
        with patch.object(a, "model_akisi", akis):
            self.ajan._modeli_cagir()
        self.assertEqual(gelen["think"], "low")


class UyarlananDusunmeTesti(ModelTesti):
    def seviye(self, *mesajlar):
        self.ajan.mesajlar = self.ajan.mesajlar[:1] + list(mesajlar)
        return self.ajan._uyarlanan_seviye()

    def test_karar_adimlari_orta_mekanik_adimlar_az(self):
        self.ajan.dusun, self.ajan.dusunme_seviyesi = True, "uyarlanir"
        arac = lambda ad, m: {"role": "tool", "tool_name": ad, "content": m}  # noqa: E731
        self.assertEqual(self.seviye({"role": "user", "content": "duzelt"}), "medium", "turun basi")
        self.assertEqual(self.seviye(arac("read_file", "1\tx = 1")), "low")
        self.assertEqual(self.seviye(arac("edit_file", "a.py duzenlendi")), "low")
        self.assertEqual(self.seviye(arac("run_command", "OK\n[cikis kodu: 0]")), "low", "gecen test")
        self.assertEqual(self.seviye(arac("run_command", "FAIL\n[cikis kodu: 1]")), "medium", "basarisiz test")
        self.assertEqual(self.seviye(arac("edit_file", "HATA: old_text bulunamadi")), "medium")
        self.assertEqual(self.seviye(arac("edit_file", a.REDDEDILDI)), "medium")
        self.assertEqual(self.seviye(arac("read_file", a.TEKRAR_NOTU)), "medium")
        self.assertEqual(self.seviye(arac("read_file", "x"), {"role": "user", "content": a.BUTCE_NOTU}), "medium",
                         "hatirlatma notu karar ister")
        self.ajan.mesajlar = self.ajan.mesajlar[:1] + [arac("read_file", "x")]
        self.assertEqual(self.ajan._think(), "low", "_think uyarlanani kullanir")


class DusunmeSiniriTesti(ModelTesti):
    def akis(self, *cevaplar):
        """Her model cagrisi icin sirayla bir parca listesi doner; cagrilarin think degerini kaydeder."""
        sira = iter(cevaplar)
        self.thinkler, self.kapatildi = [], []

        def akis(model, mesajlar, baglam, dusun=False, araclar=True):
            self.thinkler.append(dusun)
            try:
                yield from next(sira, [{"message": {"content": "tamam"}, "done": True}])
            finally:
                self.kapatildi.append(True)
        return patch.object(a, "model_akisi", akis)

    def test_aralikli_kesintiler_turu_durdurmaz(self):
        """Sayac yalniz art arda kesintileri sayar; araya basarili bir cevap girince sifirlanir."""
        self.ajan.dusun = True
        uzun = [{"message": {"thinking": "x" * 31_000}}]
        arac = [{"message": {"tool_calls": [{"function": {"name": "list_files", "arguments": {}}}]}, "done": True}]
        with self.akis(uzun, arac, uzun, uzun, arac, uzun, uzun, arac):
            self.assertTrue(self.ajan.tur("bir sey yap"), "toplam 5 kesinti ama hic 3 art arda yok")
        self.assertEqual(len([m for m in self.ajan.mesajlar if m.get("content") == a.UZUN_DUSUNME_NOTU]), 5)
        self.assertEqual(self.ajan.arayuz.hatalar, [])

    def test_uzun_dusunme_kesilir_kisa_dusunerek_yeniden_denenir(self):
        self.ajan.dusun = True
        uzun = [{"message": {"thinking": "x" * 1000}} for _ in range(40)]  # 40.000 karakter
        with self.akis(uzun, [{"message": {"content": "tamam"}, "done": True}]):
            self.assertTrue(self.ajan.tur("bir sey yap"))
        self.assertEqual(self.thinkler[:2], [True, "low"], "ikinci deneme kisa dusunmeli")
        self.assertTrue(all(t is True for t in self.thinkler[2:]), "tek seferlik: sonraki adimlar yine normal")
        self.assertTrue([m for m in self.ajan.mesajlar if m.get("content") == a.UZUN_DUSUNME_NOTU])
        self.assertTrue(self.kapatildi, "akis kapatilmali ki Ollama uretmeyi biraksin")

    @patch.dict(os.environ, {"AIRGAP_LANG": "tr"})  # checks the Turkish UI text
    def test_art_arda_uzun_dusunme_turu_bitirir(self):
        self.ajan.dusun = True
        uzun = [{"message": {"thinking": "x" * 31_000}}]
        with self.akis(uzun, uzun, uzun):
            self.assertFalse(self.ajan.tur("bir sey yap"))
        self.assertIn("cok uzun", self.ajan.arayuz.hatalar[-1])

    def test_normal_dusunme_kesilmez(self):
        self.ajan.dusun = True
        with self.akis([{"message": {"thinking": "y" * 5000}}, {"message": {"content": "tamam"}, "done": True}]):
            self.assertTrue(self.ajan.tur("x"))
        self.assertTrue(all(t is True for t in self.thinkler), "kisa dusunmeye gecilmemeli")
        self.assertFalse([m for m in self.ajan.mesajlar if m.get("content") == a.UZUN_DUSUNME_NOTU])

    def test_bozuk_cagrida_akan_metin_geri_cekilir(self):
        olaylar = []
        self.ajan.arayuz.ara_not = lambda: olaylar.append("ara_not")
        self.kurgula(a.ModelHatasi("error parsing tool call: raw='We wrote'"), yanit("bitti", read_file={"path": "a.py"}), yanit("bitti"))
        self.assertTrue(self.ajan.tur("isle"))
        self.assertIn("ara_not", olaylar)


class CiftCevapTesti(ModelTesti):
    """Gercek denemede: ajan hatirlatinca model cevabini tekrarladi, panelde iki balon oldu."""

    def test_hatirlatmadan_onceki_cevap_geri_cekilir(self):
        olaylar = []
        self.ajan.arayuz.ara_not = lambda: olaylar.append("ara_not")
        self.kurgula(yanit("_tutar"), yanit("_tutar"))
        self.assertTrue(self.ajan.tur("ilk fonksiyon neydi"))
        self.assertEqual(olaylar, ["ara_not"], "ilk cevap dusunce kutusuna alinmali, ikincisi kalmali")

    def test_icerik_verildiyse_arac_hatirlatmasi_yok(self):
        istek, _ = self.ajan.baglamli_istek("@a.py ne yapar", None)
        self.kurgula(yanit("x'i 1 yapar"))
        self.assertTrue(self.ajan.tur(istek))
        self.assertFalse([m for m in self.ajan.mesajlar if "You called no tools" in (m.get("content") or "")])
        istek, _ = self.ajan.baglamli_istek("bu ne", {"yol": "a.py", "secim": {"bas": 1, "son": 1, "metin": "x = 1"}})
        self.kurgula(yanit("atama"))
        self.assertTrue(self.ajan.tur(istek))
        self.assertFalse([m for m in self.ajan.mesajlar if "You called no tools" in (m.get("content") or "")])

    def test_yalniz_acik_dosya_adi_verildiyse_hatirlatma_surer(self):
        istek, _ = self.ajan.baglamli_istek("bu dosyada hata var mi", {"yol": "a.py", "satir": 1})
        self.kurgula(yanit("yok"), yanit("yok"))
        self.assertTrue(self.ajan.tur(istek))
        self.assertTrue([m for m in self.ajan.mesajlar if "You called no tools" in (m.get("content") or "")])

    def test_tek_cevapta_geri_cekme_yok(self):
        olaylar = []
        self.ajan.arayuz.ara_not = lambda: olaylar.append("ara_not")
        self.kurgula(yanit(read_file={"path": "a.py"}), yanit("x 1 dir"))
        self.assertTrue(self.ajan.tur("x nedir"))
        self.assertEqual(olaylar, [])


class InceleneHatalarTesti(unittest.TestCase):
    """Bagimsiz kod incelemesinde bulunan ve dogrulanan hatalar."""

    def setUp(self):
        self.g = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.g, ignore_errors=True)
        self.a = a.Araclar(self.g)

    def test_metin_olmayan_icerik_cokertmez(self):
        for ad, arg in [("write_file", {"path": "p.json", "content": {"ad": 1}}),
                        ("edit_file", {"path": "p.json", "old_text": ["x"], "new_text": "y"}),
                        ("read_file", {"path": 5})]:
            with self.subTest(ad=ad):
                s = self.a.calistir(ad, arg)
                self.assertTrue(s.startswith("HATA"), s)
        self.assertIn("metin (string) olmali", self.a.calistir("write_file", {"path": "p.json", "content": {"ad": 1}}))
        self.assertFalse((self.g / "p.json").exists())

    def test_utf8_olmayan_dosya_bozulmaz(self):
        ham = "şeker çay\nx\n".encode("cp1254")
        (self.g / "eski.txt").write_bytes(ham)
        s = self.a.calistir("edit_file", {"path": "eski.txt", "old_text": "x", "new_text": "y"})
        self.assertIn("UTF-8 degil", s)
        self.assertEqual((self.g / "eski.txt").read_bytes(), ham, "dosya hic degismemeli")

    @unittest.skipIf(os.name == "nt" and not os.environ.get("CI"), "Windows'ta symlink icin yonetici izni gerekir")
    def test_kisayol_proje_disini_veya_gizliyi_aratmaz(self):
        dis = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, dis, ignore_errors=True)
        (dis / "d.txt").write_text("PROJE_DISI_ISARET\n", encoding="utf-8")
        (self.g / ".env").write_text("GIZLI_ISARET\n", encoding="utf-8")
        (self.g / "ic.txt").write_text("IC_ISARET\n", encoding="utf-8")
        try:
            os.symlink(dis / "d.txt", self.g / "notlar.md")
            os.symlink(self.g / ".env", self.g / "ayar.md")
            os.symlink(self.g / "ic.txt", self.g / "kopya.md")
        except OSError:
            self.skipTest("symlink olusturulamadi")
        self.assertEqual(self.a.calistir("search_text", {"pattern": "PROJE_DISI|GIZLI"}), "(sonuc yok)")
        self.assertIn("kopya.md", self.a.calistir("search_text", {"pattern": "IC_ISARET"}), "proje ici kisayol aranir")

    def test_kisayol_kontrolu_taklitle(self):
        # Windows'ta symlink olusturulamasa da ayni yolu sinar.
        (self.g / "notlar.md").write_text("x", encoding="utf-8")
        (self.g / "ic.md").write_text("x", encoding="utf-8")
        dis = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, dis, ignore_errors=True)
        asil_resolve = Path.resolve

        def sahte_resolve(y, *x, **k):
            if y.name == "notlar.md":
                return dis / "d.txt"
            if y.name == "ic.md":
                return asil_resolve(self.g, *x, **k) / ".env"
            return asil_resolve(y, *x, **k)
        with patch.object(Path, "is_symlink", lambda y: y.name in ("notlar.md", "ic.md")), \
                patch.object(Path, "resolve", sahte_resolve):
            self.assertFalse(self.a.guvenli_dosya(self.g / "notlar.md"), "proje disi")
            self.assertFalse(self.a.guvenli_dosya(self.g / "ic.md"), "gizli dosyaya giden")
            self.assertTrue(self.a.guvenli_dosya(self.g / "baska.md"), "kisayol degil")

    def test_geri_alma_kisayolun_hedefini_silmez(self):
        os.environ.setdefault("KOD_AJANI_VERI", str(self.g / "veri"))
        kok = self.g / "p"
        (kok / "src").mkdir(parents=True)
        (kok / "src" / "ana.py").write_text("x = 1\n", encoding="utf-8")
        g = a.GeriAlma(kok)
        sahte_hedef = kok / "src" / "ana.py"
        # Kisayolun kendisi cozulmeden silinmeli; cozulmus yol silinseydi ana.py giderdi.
        (kok / "link.py").write_text("kisayol yerine\n", encoding="utf-8")
        asil = Path.resolve
        with patch.object(Path, "resolve", lambda y, *x, **k: sahte_hedef if y.name == "link.py" else asil(y, *x, **k)):
            g._eklenen_sil("link.py")
        self.assertFalse((kok / "link.py").exists())
        self.assertTrue(sahte_hedef.exists(), "kisayolun gosterdigi dosya silinmemeli")

    def test_bitmis_komutun_numarasina_dokunulmaz(self):
        surec = __import__("subprocess").Popen([sys.executable, "-c", "pass"], stdout=__import__("subprocess").PIPE)
        surec.communicate()
        self.a.surec = surec
        with patch.object(a, "surec_agacini_durdur") as durdur:
            self.a.durdur()
        durdur.assert_not_called()

    def test_zaman_asiminda_ikinci_bekleme_sinirli(self):
        import subprocess as sp
        cagrilar = []

        class SahteSurec:
            pid, returncode, stdout = 1, None, None

            def communicate(self, timeout=None):
                cagrilar.append(timeout)
                raise sp.TimeoutExpired("x", timeout)

            def poll(self):
                return None
        with patch.object(a.subprocess, "Popen", lambda *x, **k: SahteSurec()), \
                patch.object(a, "surec_agacini_durdur"):
            s = self.a.run_command("python uzun.py")
        self.assertIn("durduruldu", s)
        self.assertEqual(cagrilar, [a.KOMUT_ZAMAN_ASIMI, 10], "ikinci bekleme de sinirli olmali")


if __name__ == "__main__":
    unittest.main()
