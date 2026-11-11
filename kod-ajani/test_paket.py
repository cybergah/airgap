import json
import re
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import paketle as p


class PaketTesti(unittest.TestCase):
    def setUp(self):
        gecici = tempfile.TemporaryDirectory()
        self.addCleanup(gecici.cleanup)
        self.vsix = p.paketle(Path(gecici.name))
        self.z = zipfile.ZipFile(self.vsix)
        self.addCleanup(self.z.close)

    def test_gerekli_dosyalar_var_testler_yok(self):
        adlar = set(self.z.namelist())
        self.assertLessEqual({"extension.vsixmanifest", "[Content_Types].xml", "extension/package.json",
                              "extension/extension.js", "extension/ajan.py", "extension/media/panel.js"}, adlar)
        self.assertFalse([a for a in adlar if "test" in a or "__pycache__" in a])

    def test_manifest_gecerli_ve_surum_uyumlu(self):
        kok = ElementTree.fromstring(self.z.read("extension.vsixmanifest"))
        kimlik = kok.find("{*}Metadata/{*}Identity")
        bilgi = json.loads(self.z.read("extension/package.json"))
        self.assertEqual(kimlik.get("Version"), bilgi["version"])
        self.assertEqual(kimlik.get("Id"), bilgi["name"])
        self.assertEqual(kimlik.get("Publisher"), bilgi["publisher"])

    def test_panelin_istedigi_dosyalar_pakette(self):
        kod = self.z.read("extension/extension.js").decode("utf-8")
        for ad in re.findall(r'uri\("([\w.]+)"\)', kod):
            self.assertIn(f"extension/media/{ad}", self.z.namelist())
        self.assertIn("extension/media/ikon.svg", self.z.namelist())

    def test_pakettaki_ajan_guncel(self):
        self.assertEqual(self.z.read("extension/ajan.py"), (p.BURASI / "ajan.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
