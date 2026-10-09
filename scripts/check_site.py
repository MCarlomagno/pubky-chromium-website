"""Check the static download page and its release metadata contract."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re

ROOT = Path(__file__).resolve().parents[1] / "docs"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            assert values["id"] not in self.ids, "Duplicate element ID"
            self.ids.add(values["id"])
        if tag == "a":
            self.links.append(values.get("href", ""))
        if tag in ("img", "script", "link"):
            ref = values.get("src") or values.get("href")
            if ref:
                self.images.append(ref)


page = (ROOT / "index.html").read_text()
references = References()
references.feed(page)
repo = "https://github.com/MCarlomagno/pubky-chromium"
mac_tag = "pubky-macos-156.0.8073.3"
mac_asset = "pubky-chromium-156.0.8073.3-macos-arm64.zip"
linux_tag = "pubky-linux-156.0.8073.2"
linux_asset = "pubky-chromium_156.0.8073.2-1_amd64.deb"
windows_tag = "pubky-156.0.8073.1"
windows_asset = "pubky-chromium-156.0.8073.1-windows-x64-mini-installer.exe"
assert f"{repo}/releases/download/{mac_tag}/{mac_asset}" in references.links
assert f"{repo}/releases/download/{linux_tag}/{linux_asset}" in references.links
assert f"{repo}/releases/download/{windows_tag}/{windows_asset}" in references.links
assert f"{repo}/commit/e8c5d30f605f322b1f4688e1f2cb42d54ddc305b" in references.links
assert f"{repo}/commit/c1136b720ca25952fa1e2d4eef545b1575163a6b" in references.links
assert f"{repo}/commit/50721a8b9692dd2736ab42a8d6c2e9b51f08847b" in references.links
assert re.search(r'<code id="mac-sha256">[a-f0-9]{64}</code>', page)
assert re.search(r'<code id="linux-sha256">[a-f0-9]{64}</code>', page)
assert re.search(r'<code id="windows-sha256">[a-f0-9]{64}</code>', page)
assert "Download not available yet" not in page and "@@" not in page
assert "Browser for the free internet" in page
assert "Censorship resistant" in page and "A familiar browser." not in page
assert "Try the experimental Mac build" not in page
assert "Before you install" not in page and "Install a separate test copy" not in page
assert page.count('class="download"') == 3
assert references.images and all(not urlsplit(ref).scheme for ref in references.images)
for ref in references.links + references.images:
    url = urlsplit(ref)
    if url.scheme:
        assert url.scheme == "https", ref
        continue
    assert ref and not ref.startswith("/") and ".." not in Path(url.path).parts, ref
    assert (ROOT / (url.path or "index.html")).is_file(), ref
    if url.fragment:
        assert url.fragment in references.ids, ref
assert not any(p.suffix.lower() in {".zip", ".dmg", ".pkg", ".dylib", ".deb", ".exe"} for p in ROOT.rglob("*"))
print("Site references, local assets and Mac/Linux/Windows release metadata OK")
