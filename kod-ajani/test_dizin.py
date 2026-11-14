"""Proje aramasi: Ollama olmadan, kelimelerden uretilen sahte vektorlerle."""
import hashlib
import math
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import ajan as a


def sahte_gomme(gorulen):
    def gomme(model, metinler):
        gorulen.extend(metinler)
        sonuc = []
        for metin in metinler:
            v = [0.0] * 64
            for k in re.findall(r"\w+", metin.lower()):
                if k in ("search_document", "search_query"):
                    continue
                v[int(hashlib.md5(k.encode()).hexdigest(), 16) % 64] += 1.0
            sonuc.append(v)
        return sonuc
    return gomme


class DizinTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.gecici, ignore_errors=True)
        self.kok = self.gecici / "proje"
        self.kok.mkdir()
        ortam = patch.dict(os.environ, {"KOD_AJANI_VERI": str(self.gecici / "veri")})
        ortam.start()
        self.addCleanup(ortam.stop)
        self.gorulen = []
        yama = patch.object(a, "gomme_al", sahte_gomme(self.gorulen))
        yama.start()
        self.addCleanup(yama.stop)
        self.ajan = a.Ajan(self.kok, "sahte")
        self.dizin = self.ajan.araclar.dizin

    def yaz(self, ad, icerik):
        yol = self.kok / ad
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_bytes(icerik.encode("utf-8") if isinstance(icerik, str) else icerik)

    def test_ilgili_dosya_ilk_sirada(self):
        self.yaz("indirim.py", "def kupon_indirimi(): return 'kupon indirimi hesaplanir'\n")
        self.yaz("stok.py", "def urun_stogu(): return 'depo sayimi'\n")
        self.assertEqual(self.dizin.ara("kupon indirimi")[0]["yol"], "indirim.py")

    def test_arac_sonucu_yol_ve_satir_verir(self):
        self.yaz("a.py", "def kupon(): pass\n")
        sonuc = self.ajan.araclar.calistir("search_code", {"query": "kupon"})
        self.assertIn("a.py:1-1", sonuc)
        self.assertIn("1\tdef kupon(): pass", sonuc)

    def test_ortak_onbellek_projeler_arasi_yeniden_gommez(self):
        onbellek = str(self.gecici / "ortak.sqlite3")
        self.yaz("a.py", "def kupon(): pass\n")
        with patch.dict(os.environ, {"KOD_AJANI_VEKTOR_ONBELLEK": onbellek}):
            self.assertEqual(self.dizin.guncelle()["yeni"], 1)
            ikinci = self.gecici / "kopya"
            shutil.copytree(self.kok, ikinci)
            self.gorulen.clear()
            diger = a.ProjeDizini(ikinci, lambda: ["a.py"], self.dizin.model)
            self.assertEqual(diger.guncelle()["yeni"], 0, "ayni parca ortak onbellekten gelmeli")
            self.assertEqual(self.gorulen, [])
            self.assertEqual(diger.ara("kupon")[0]["yol"], "a.py")
            baska_model = a.ProjeDizini(ikinci, lambda: ["a.py"], "baska")
            self.assertEqual(baska_model.guncelle()["yeni"], 1, "baska modelin vektoru kullanilmaz")

    def test_yalniz_degisen_dosya_yeniden_islenir(self):
        self.yaz("a.py", "bir\n")
        self.yaz("b.py", "iki\n")
        self.assertEqual(self.dizin.guncelle()["yeni"], 2)
        self.gorulen.clear()
        self.assertEqual(self.dizin.guncelle()["yeni"], 0)
        self.assertEqual(self.gorulen, [])
        self.yaz("b.py", "degisti uzun\n")
        self.assertEqual(self.dizin.guncelle()["yeni"], 1)

    def test_ayni_icerik_yeniden_gomulmez(self):
        self.yaz("a.py", "ayni\n")
        self.dizin.guncelle()
        self.yaz("alt.py", "ayni\n")
        self.assertEqual(self.dizin.guncelle()["yeni"], 1)  # yol da metne dahil, farkli belge

    def test_silinen_dosya_sonuctan_cikar(self):
        self.yaz("a.py", "kupon\n")
        self.dizin.guncelle()
        (self.kok / "a.py").unlink()
        self.assertEqual(self.dizin.ara("kupon"), [])

    def test_gitignore_ikili_ve_atlanan_dosyalar_dizine_girmez(self):
        self.yaz(".gitignore", "*.env\n")
        self.yaz("gizli.env", "PAROLA=cokgizli\n")
        self.yaz("resim.bin", b"\0\1\2kupon")
        self.yaz("node_modules/x.js", "kupon\n")
        self.yaz("buyuk.txt", "kupon\n" * 100_000)
        self.yaz("a.py", "kupon\n")
        self.dizin.guncelle()
        yollar = {s["yol"] for s in self.dizin.ara("kupon", adet=20)}
        self.assertEqual(yollar - {".gitignore"}, {"a.py"})
        self.assertFalse(any("cokgizli" in m for m in self.gorulen))

    def test_dizinde_kod_metni_saklanmaz(self):
        self.yaz("a.py", "benzersiz_gizli_metin\n")
        self.dizin.guncelle()
        self.assertNotIn(b"benzersiz_gizli_metin", self.dizin.dosya.read_bytes())

    def test_ortusen_parcalar_tekrar_etmez(self):
        self.yaz("a.py", "kupon\n" * 200)
        sonuclar = self.dizin.ara("kupon", adet=10)
        aralik = sorted((s["bas"], s["son"]) for s in sonuclar)
        for (_, son), (bas, _) in zip(aralik, aralik[1:]):
            self.assertLess(son, bas)

    def test_parcalar_ortusur_ve_bos_kalmaz(self):
        parcalar = a.parcala("\n".join(f"s{i}" for i in range(100)))
        self.assertEqual(parcalar[0][:2], (1, 40))
        self.assertEqual(parcalar[1][:2], (33, 72))
        self.assertEqual(parcalar[-1][1], 100)
        self.assertEqual(a.parcala("\n\n  \n"), [])

    def test_model_yoksa_tur_olmez_arac_hatasi_doner(self):
        self.yaz("a.py", "x\n")
        with patch.object(a, "gomme_al", side_effect=a.ModelHatasi("yok")):
            sonuc = self.ajan.araclar.calistir("search_code", {"query": "x"})
        self.assertTrue(sonuc.startswith("HATA"))
        self.assertIn("search_text", sonuc)

    def test_yarida_kesilince_islenen_kalir(self):
        for i in range(a.GOMME_TOPLU + 5):
            self.yaz(f"d{i}.py", f"icerik{i}\n")
        cagri = {"n": 0}

        def kontrol():
            cagri["n"] += 1
            if cagri["n"] == 2:
                raise KeyboardInterrupt

        self.dizin.kontrol = kontrol
        with self.assertRaises(KeyboardInterrupt):
            self.dizin.guncelle()
        self.dizin.kontrol = lambda: None
        # Ilk toplu is korunur, yalniz kalan 5 parca islenir; sonra bitmistir.
        self.assertEqual(self.dizin.guncelle()["yeni"], 5)
        self.assertEqual(self.dizin.guncelle()["yeni"], 0)
        self.assertEqual(len(self.dizin.ara("icerik", adet=100)), a.GOMME_TOPLU + 5)  # hepsi aranabilir

    def test_vektor_bire_normalize_edilir(self):
        from array import array
        v = array("f")
        v.frombytes(a._vektor_bayt([3.0, 4.0]))
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in v)), 1.0, places=5)
        self.assertIsNone(a._vektor_bayt([0.0, 0.0]))


if __name__ == "__main__":
    unittest.main()
