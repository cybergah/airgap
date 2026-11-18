"""Masaustu sunucusu: anahtarsiz, yabanci Host/Origin ya da yol kacisi istekleri reddedilir."""
import http.client
import json
import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / "masaustu"))
import uygulama as u  # noqa: E402


class MasaustuSunucuTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        veri = Path(self.gecici.name)
        # Derlenmis arayuzun yerine kucuk bir sahtesi: testler npm olmadan her isletim sisteminde calisir.
        arayuz = veri / "arayuz"
        (arayuz / "assets").mkdir(parents=True)
        (arayuz / "index.html").write_text('<meta name="kod-ajani-anahtar" content="__ANAHTAR__"><script src="./assets/a.js">',
                                           encoding="utf-8")
        (arayuz / "assets" / "a.js").write_text("1", encoding="utf-8")
        (arayuz / "logo.svg").write_text("<svg/>", encoding="utf-8")
        for ad, deger in (("VERI", veri), ("AYAR_DOSYASI", veri / "ayarlar.json"), ("ARAYUZ", arayuz)):
            p = patch.object(u, ad, deger)
            p.start()
            self.addCleanup(p.stop)
        self.uyg = u.Uygulama()
        self.sunucu = u.Sunucu(("127.0.0.1", 0), None)
        self.port = self.sunucu.server_address[1]
        self.sunucu.RequestHandlerClass = u.isleyici(self.uyg, self.port)
        threading.Thread(target=self.sunucu.serve_forever, daemon=True).start()
        self.addCleanup(self.sunucu.server_close)
        self.addCleanup(self.sunucu.shutdown)

    def istek(self, yontem, yol, govde=None, basliklar=None):
        b = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        b.request(yontem, yol, body=govde, headers=basliklar or {})
        y = b.getresponse()
        icerik = y.read()
        b.close()
        return y.status, icerik

    def test_dil_ayar_sonra_airgap_lang(self):
        with patch.dict(os.environ, {"AIRGAP_LANG": "tr"}):
            self.assertEqual(self.uyg.dil(), "tr")
            self.uyg.ayar["dil"] = "en"
            self.assertEqual(self.uyg.dil(), "en", "ayar ortam degiskeninden once gelir")
        self.uyg.ayar["dil"] = ""
        with patch.dict(os.environ, {"AIRGAP_LANG": "en"}):
            self.assertEqual(self.uyg.L("Kaydet", "Save"), "Save")

    def test_sayfa_anahtar_ister(self):
        self.assertEqual(self.istek("GET", "/")[0], 403)
        self.assertEqual(self.istek("GET", "/?t=yanlis")[0], 403)
        kod, govde = self.istek("GET", f"/?t={self.uyg.anahtar}")
        self.assertEqual(kod, 200)
        self.assertIn(self.uyg.anahtar.encode(), govde, "anahtar sayfaya gomulur")
        self.assertNotIn(b"__ANAHTAR__", govde)

    def test_yabanci_host_ve_origin_reddedilir(self):
        t = self.uyg.anahtar
        self.assertEqual(self.istek("GET", f"/?t={t}", basliklar={"Host": f"kotu.example:{self.port}"})[0], 403)
        self.assertEqual(self.istek("POST", f"/komut?t={t}", b"{}", {"Origin": "http://kotu.example"})[0], 403)

    def test_komut_anahtarsiz_islenmez(self):
        with patch.object(self.uyg, "panel_mesaji") as islem:
            self.assertEqual(self.istek("POST", "/komut", json.dumps({"tur": "mesaj", "metin": "x"}).encode())[0], 403)
            islem.assert_not_called()
            self.assertEqual(self.istek("POST", f"/komut?t={self.uyg.anahtar}", b'{"tur": "dur"}')[0], 204)
            islem.assert_called_once()

    def test_yalniz_izinli_dosyalar_sunulur(self):
        self.assertEqual(self.istek("GET", "/assets/a.js")[0], 200)
        self.assertEqual(self.istek("GET", "/logo.svg")[0], 200)
        for yol in ("/assets/..%2f..%2fajanlar.json", "/assets/../ayarlar.json", "/..%2fayarlar.json", "/ayarlar.json",
                    "/assets/yok.js", "/masaustu/uygulama.py"):
            self.assertEqual(self.istek("GET", yol)[0], 404, yol)

    def test_ayar_yalniz_bilinen_alanlari_kabul_eder(self):
        self.uyg.panel_mesaji({"tur": "ayar_kaydet", "ayar": {"model": "qwen", "maks_adim": "cok", "python": "kotu.exe",
                                                             "korumali": True}})
        self.assertEqual(self.uyg.ayar["model"], "qwen")
        self.assertEqual(self.uyg.ayar["maks_adim"], 40, "yanlis turdeki deger alinmaz")
        self.assertNotIn("python", self.uyg.ayar)
        self.assertTrue(json.loads((u.VERI / "ayarlar.json").read_text(encoding="utf-8"))["korumali"])

    def test_ollama_adresi_dinleme_adresinden_baglanma_adresine(self):
        for deger, beklenen in (("0.0.0.0:11434", "http://127.0.0.1:11434"), ("", "http://127.0.0.1:11434"),
                                ("http://10.0.0.5:9000/", "http://10.0.0.5:9000"), ("[::]:11434", "http://127.0.0.1:11434")):
            with patch.dict(os.environ, {"OLLAMA_HOST": deger}):
                self.assertEqual(u.ollama_adresi(), beklenen, deger)

    def test_bomlu_ayar_dosyasi_okunur(self):
        (u.VERI / "ayarlar.json").write_text('{"model": "qwen3:8b"}', encoding="utf-8-sig")
        self.assertEqual(u.ayar_oku()["model"], "qwen3:8b")

    def test_dosya_listesi_gizli_ve_atlanan_dosyalari_vermez(self):
        k = Path(self.gecici.name) / "proje"
        for ad in ("a.py", "alt/b.js", ".env", "id_rsa", "node_modules/x/y.js", ".git/config", "anahtar.pem"):
            (k / ad).parent.mkdir(parents=True, exist_ok=True)
            (k / ad).write_text("x", encoding="utf-8")
        self.assertEqual(u.proje_dosyalari(str(k)), ["a.py", "alt/b.js"])

    @unittest.skipUnless(os.name == "nt", "Gezgin yalniz Windows'ta")
    def test_goster_proje_disina_cikmaz(self):
        k = Path(self.gecici.name) / "proje"
        k.mkdir()
        (k / "a.py").write_text("x", encoding="utf-8")
        self.uyg.klasor = str(k)
        with patch.object(u.subprocess, "Popen") as ac:
            self.uyg.panel_mesaji({"tur": "goster", "yol": "../ayarlar.json"})
            self.uyg.panel_mesaji({"tur": "goster", "yol": "yok.py"})
            ac.assert_not_called()
            self.uyg.panel_mesaji({"tur": "goster", "yol": "a.py"})
            self.assertEqual(ac.call_args[0][0][0], "explorer.exe")

    def test_klasor_gecmisi_klasore_ozel(self):
        a, b = Path(self.gecici.name) / "a", Path(self.gecici.name) / "b"
        a.mkdir(), b.mkdir()
        self.uyg.klasor_ac(str(a), yayinla=False)
        self.uyg.gecmis = [{"tur": "kullanici", "metin": "merhaba"}]
        self.uyg.gecmis_kaydet()
        self.uyg.klasor_ac(str(b), yayinla=False)
        self.assertEqual(self.uyg.gecmis, [])
        self.uyg.klasor_ac(str(a), yayinla=False)
        self.assertEqual(self.uyg.gecmis[0], {"tur": "kullanici", "metin": "merhaba"})
        self.assertEqual(self.uyg.ayar["son_klasorler"][:2], [os.path.abspath(a), os.path.abspath(b)])


if __name__ == "__main__":
    unittest.main()
