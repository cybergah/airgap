"""Statik denetim: calistirmadan yakalanan hatalar ve ajanin "bitti" anindaki davranisi."""
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a
from test_saglamlik import ModelTesti, yanit


class StatikTesti(unittest.TestCase):
    def setUp(self):
        self.kok = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.kok, ignore_errors=True)

    def sorunlar(self, **dosyalar):
        for ad, icerik in dosyalar.items():
            yol = self.kok / ad
            yol.parent.mkdir(parents=True, exist_ok=True)
            yol.write_text(icerik, encoding="utf-8")
        liste = [p.relative_to(self.kok).as_posix() for p in self.kok.rglob("*.py")]
        return sorted((a.statik_sorunlar(self.kok, liste) or {}).values())

    def test_temiz_proje_sorunsuz(self):
        self.assertEqual(self.sorunlar(**{
            "para/__init__.py": "",
            "para/vergi.py": "ORAN = 0.2\n\n\ndef kdv_ekle(t, oran=ORAN):\n    return t * (1 + oran)\n",
            "para/fatura.py": "from para.vergi import kdv_ekle\n\n\ndef fatura(t):\n    return kdv_ekle(t)\n",
            "para/rapor.py": "from para import vergi\n\n\ndef rapor(t):\n    return f'{vergi.kdv_ekle(t):.2f}'\n"}), [])

    def test_yarim_kalan_yeniden_adlandirma_uc_bicimde_yakalanir(self):
        s = self.sorunlar(**{
            "para/__init__.py": "",
            "para/vergi.py": "def kdv_ekle(t):\n    return t * 1.2\n",
            "para/fatura.py": "from para.vergi import kdv_ekle\n\n\ndef fatura(t):\n    return hesapla_kdv(t)\n",
            "para/rapor.py": "from para import vergi\n\n\ndef rapor(t):\n    return vergi.hesapla_kdv(t)\n",
            "para/eski.py": "from .vergi import hesapla_kdv\n"})
        self.assertEqual(len(s), 3, s)
        self.assertIn("para/fatura.py:5: name 'hesapla_kdv' is not defined", s)
        self.assertTrue(any("rapor.py:5: module 'vergi'" in x and "no attribute 'hesapla_kdv'" in x for x in s), s)
        self.assertTrue(any("eski.py:1: cannot import name 'hesapla_kdv'" in x for x in s), s)

    def test_arguman_sayisi(self):
        s = self.sorunlar(**{
            "model.py": "class Kullanici:\n    def __init__(self, ad, eposta, telefon):\n        self.ad = ad\n",
            "dogrula.py": "from model import Kullanici\n\n\ndef olustur(ad, eposta):\n    return Kullanici(ad, eposta)\n\n\n"
                          "def iki():\n    return olustur('a', 'b', 'c')\n\n\ndef uc():\n    return olustur('a', eposta='b', yas=3)\n"})
        self.assertEqual(len(s), 3, s)
        self.assertTrue(any("dogrula.py:5: Kullanici() is called without required argument(s): telefon" in x for x in s), s)
        self.assertTrue(any("olustur() takes 2 positional argument(s) but 3 were given" in x for x in s), s)
        self.assertTrue(any("unexpected keyword argument(s): yas" in x for x in s), s)

    def test_emin_olunamayan_durumlarda_susar(self):
        self.assertEqual(self.sorunlar(**{
            "a.py": "from b import *\nprint(bilinmeyen)\n",                                   # yildizli import
            "b.py": "import functools\n\n\n@functools.cache\ndef f(x):\n    return x\n",
            "c.py": "from b import f\nf(1, 2, 3)\n",                                           # susleyicili: imza degisebilir
            "d.py": "def g(*a, **k):\n    return a\n\n\ng(1, 2, x=3)\nargs = (1,)\ng(*args)\n",
            "e.py": "try:\n    from b import yok\nexcept ImportError:\n    yok = None\n",        # istege bagli import
            "f.py": "import json\nimport os.path\n\n\ndef h(vergi):\n    return vergi.olmayan + json.dumps(1) + len(os.sep)\n",
            "g.py": "def top(self, which):\n    return which\n",                              # CPython 'top' tuhafligi
            "h.py": "class T:\n    x = 1\n\n    def m(self):\n        return [self.x for _ in range(2)]\n",
            "i.py": "import abc\n\n\nclass K(abc.ABC):\n    pass\n", "abc.py": "x = 1\n",    # stdlib adi, yandaki dosya degil
            "j.py": "try:\n    get_ipython()\nexcept NameError:\n    pass\n"}), [])

    def test_bozuk_dosya_ve_buyuk_proje(self):
        self.assertEqual(self.sorunlar(**{"bozuk.py": "def (:\n", "iyi.py": "x = 1\n"}), [])
        with patch.object(a, "STATIK_DOSYA_SINIRI", 1):
            self.assertIsNone(a.statik_sorunlar(self.kok, ["bozuk.py", "iyi.py"]))

    def test_anahtar_satir_numarasi_icermez(self):
        self.sorunlar(**{"a.py": "print(yok)\n"})
        once = a.statik_sorunlar(self.kok, ["a.py"])
        (self.kok / "a.py").write_text("\n\n\nprint(yok)\n", encoding="utf-8")
        self.assertEqual(set(once), set(a.statik_sorunlar(self.kok, ["a.py"])), "satiri kayan eski sorun yeni sayilmamali")


class StatikAjanTesti(ModelTesti):
    def setUp(self):
        super().setUp()
        (self.kok / "vergi.py").write_text("def hesapla_kdv(t):\n    return t * 1.2\n", encoding="utf-8")
        (self.kok / "fatura.py").write_text("from vergi import hesapla_kdv\n\n\ndef fatura(t):\n    return hesapla_kdv(t)\n",
                                            encoding="utf-8")
        (self.kok / "eski.py").write_text("print(zaten_bozuk)\n", encoding="utf-8")

    AD = {"edit_file": {"path": "vergi.py", "old_text": "def hesapla_kdv", "new_text": "def kdv_ekle"}}
    IMPORT = {"edit_file": {"path": "fatura.py", "old_text": "from vergi import hesapla_kdv", "new_text": "from vergi import kdv_ekle"}}
    CAGRI = {"edit_file": {"path": "fatura.py", "old_text": "return hesapla_kdv(t)", "new_text": "return kdv_ekle(t)"}}

    def notlar(self):
        return [m["content"] for m in self.ajan.mesajlar if m.get("role") == "user" and "[Automatic check]" in m["content"]]

    def test_yarim_is_modele_geri_verilir_duzelince_biter(self):
        self.kurgula(yanit(**self.AD), yanit(**self.IMPORT), yanit("Hepsi tamam."), yanit(**self.CAGRI), yanit("Bitti."))
        self.assertTrue(self.ajan.tur("adini degistir"))
        notlar = self.notlar()
        self.assertEqual(len(notlar), 1, notlar)
        self.assertIn("fatura.py:5: name 'hesapla_kdv' is not defined", notlar[0])
        self.assertNotIn("zaten_bozuk", notlar[0], "tur oncesinden kalan sorun bildirilmez")
        self.assertEqual(self.ajan.mesajlar[-1]["content"], "Bitti.")
        self.assertIn("return kdv_ekle(t)", (self.kok / "fatura.py").read_text(encoding="utf-8"))

    def test_temiz_duzenlemede_ve_soruda_not_yok(self):
        self.kurgula(yanit(**self.AD), yanit(**self.IMPORT), yanit(**self.CAGRI), yanit("Bitti."))
        self.assertTrue(self.ajan.tur("adini degistir"))
        self.assertEqual(self.notlar(), [])
        self.kurgula(yanit(read_file={"path": "eski.py"}), yanit("Bu dosya bozuk."))
        self.assertTrue(self.ajan.tur("eski.py nedir"))
        self.assertEqual(self.notlar(), [])

    def test_model_duzeltmezse_sinirdan_sonra_tur_biter(self):
        self.kurgula(yanit(**self.AD), yanit("Tamam."), yanit("Yanlis alarm."), yanit("Yanlis alarm."), yanit("fazla"))
        self.assertTrue(self.ajan.tur("adini degistir"))
        self.assertEqual(len(self.notlar()), a.STATIK_DOGRULAMA)
        self.assertEqual(self.ajan.mesajlar[-1]["content"], "Yanlis alarm.")

    def test_kapatilabilir(self):
        with patch.object(a, "STATIK_ACIK", False):
            self.kurgula(yanit(**self.AD), yanit("Tamam."))
            self.assertTrue(self.ajan.tur("adini degistir"))
        self.assertEqual(self.notlar(), [])


if __name__ == "__main__":
    unittest.main()


class DusunceSaklamaTesti(ModelTesti):
    """gpt-oss araclar arasinda kendi dusuncesini geri gormeli; yoksa ayni aramayi tekrar ediyordu."""

    def akis(self, *cevaplar):
        sira = iter(cevaplar)
        self.giden = []

        def akis(model, mesajlar, baglam, dusun=False, araclar=True):
            self.giden.append([dict(m) for m in mesajlar])
            yield from next(sira)
        return patch.object(a, "model_akisi", akis)

    def test_arac_cagrisinin_dusuncesi_saklanir_son_cevabinki_saklanmaz(self):
        self.ajan.dusun = True
        cagri = [{"message": {"thinking": "Plan: once a.py'yi oku, "}}, {"message": {"thinking": "sonra duzelt."}},
                 {"message": {"tool_calls": [{"function": {"name": "read_file", "arguments": {"path": "a.py"}}}]}, "done": True}]
        son = [{"message": {"thinking": "Bitti sayilir."}}, {"message": {"content": "tamam"}, "done": True}]
        with self.akis(cagri, son):
            self.assertTrue(self.ajan.tur("bak"))
        asistan = [m for m in self.giden[1] if m["role"] == "assistant"]
        self.assertEqual(asistan[-1].get("thinking"), "Plan: once a.py'yi oku, sonra duzelt.", "ikinci cagriya gitmeli")
        self.assertNotIn("thinking", self.ajan.mesajlar[-1])

    def test_kapaliyken_saklanmaz(self):
        self.ajan.dusun = True
        cagri = [{"message": {"thinking": "x"}},
                 {"message": {"tool_calls": [{"function": {"name": "read_file", "arguments": {"path": "a.py"}}}]}, "done": True}]
        with patch.object(a, "DUSUNCE_SAKLA", False), self.akis(cagri, [{"message": {"content": "tamam"}, "done": True}]):
            self.assertTrue(self.ajan.tur("bak"))
        self.assertFalse([m for m in self.ajan.mesajlar if m.get("thinking")])

    def test_baglam_dolunca_once_eski_dusunceler_silinir(self):
        m = [{"role": "system", "content": "s"}]
        for i in range(10):
            m += [{"role": "assistant", "content": "", "thinking": "d" * 1000, "tool_calls": []},
                  {"role": "tool", "content": f"sonuc {i} " + "x" * 300}]
        a.gecmisi_sigdir(m, 0, 7000)  # hedef 7000 * KIRPMA_ORANI = 4200 karakter
        self.assertTrue(all(len(t["content"]) > 300 for t in m if t["role"] == "tool"), "arac sonuclari korunmali")
        self.assertLessEqual(sum(len(x.get("thinking", "")) for x in m), 4200 - 3100)
        self.assertIn("thinking", m[-2], "en yeni dusunce kalir")

    def test_kayitli_sohbete_dusunce_yazilmaz(self):
        self.ajan.mesajlar.append({"role": "assistant", "content": "", "thinking": "gizli plan", "tool_calls": []})
        self.ajan.sohbet_kaydet()
        self.assertNotIn("gizli plan", self.ajan.sohbet_dosyasi.read_text(encoding="utf-8"))


class OkumaAdlariTesti(unittest.TestCase):
    def test_line_start_line_end_kabul_edilir(self):
        kok = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, kok, ignore_errors=True)
        (kok / "a.py").write_text("".join(f"s{i}\n" for i in range(1, 11)), encoding="utf-8")
        ar = a.Araclar(kok)
        self.assertEqual(ar.calistir("read_file", {"path": "a.py", "line_start": 3, "line_end": 4}), "3\ts3\n4\ts4")
        self.assertEqual(ar.calistir("read_file", {"path": "a.py", "start_line": 9, "end_line": 200}), "9\ts9\n10\ts10")
        self.assertTrue(ar.calistir("read_file", {"path": "a.py", "line_start": 1, "line_end": 200}).endswith("10\ts10"))
        self.assertEqual(ar.calistir("read_file", {"path": "a.py", "offset": 2, "limit": 1}), "2\ts2")
