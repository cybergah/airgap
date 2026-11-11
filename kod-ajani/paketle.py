#!/usr/bin/env python3
"""Eklentiyi ek arac gerektirmeden .vsix paketi yapar; ajan.py paketin icine girer.

    python paketle.py
    code --install-extension ../dist/kod-ajani-<surum>.vsix --force
"""
import json
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

BURASI = Path(__file__).resolve().parent
EKLENTI = BURASI / "vscode-eklenti"
PAKET_DOSYALARI = ["package.json", "extension.js", "media/panel.js", "media/panel.css", "media/ikon.svg"]
ICERIK_TURLERI = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension=".json" ContentType="application/json"/>
<Default Extension=".js" ContentType="application/javascript"/>
<Default Extension=".css" ContentType="text/css"/>
<Default Extension=".svg" ContentType="image/svg+xml"/>
<Default Extension=".py" ContentType="text/plain"/>
<Default Extension=".vsixmanifest" ContentType="text/xml"/>
</Types>
"""


def manifest(p: dict) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
<Metadata>
<Identity Language="en-US" Id={quoteattr(p["name"])} Version={quoteattr(p["version"])} Publisher={quoteattr(p["publisher"])}/>
<DisplayName>{escape(p["displayName"])}</DisplayName>
<Description xml:space="preserve">{escape(p["description"])}</Description>
<Categories>Other</Categories>
<Properties><Property Id="Microsoft.VisualStudio.Code.Engine" Value={quoteattr(p["engines"]["vscode"])}/></Properties>
</Metadata>
<Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
<Dependencies/>
<Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/></Assets>
</PackageManifest>
"""


def paketle(hedef_klasor: Path | None = None) -> Path:
    bilgi = json.loads((EKLENTI / "package.json").read_text(encoding="utf-8"))
    klasor = hedef_klasor or BURASI.parent / "dist"
    klasor.mkdir(parents=True, exist_ok=True)
    hedef = klasor / f"{bilgi['name']}-{bilgi['version']}.vsix"
    with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ICERIK_TURLERI)
        z.writestr("extension.vsixmanifest", manifest(bilgi))
        for ad in PAKET_DOSYALARI:
            z.write(EKLENTI / ad, f"extension/{ad}")
        z.write(BURASI / "ajan.py", "extension/ajan.py")
    return hedef


if __name__ == "__main__":
    print(paketle())
    sys.exit(0)
