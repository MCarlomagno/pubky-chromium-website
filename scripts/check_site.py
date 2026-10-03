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
tag = "macos-arm64-156.0.8073.0-d3d736b0"
asset = "pubky-chromium-156.0.8073.0-macos-arm64.zip"
assert f"{repo}/releases/download/{tag}/{asset}" in references.links
assert f"{repo}/releases/download/{tag}/SHA256SUMS.txt" in references.links
assert f"{repo}/releases/tag/{tag}" in references.links
assert f"{repo}/commit/d3d736b050b7fdd67010979ccbcab6cca76d63eb" in references.links
assert re.search(r'<code id="sha256">[a-f0-9]{64}</code>', page)
assert "Download not available yet" not in page and "@@" not in page
assert "Not notarized by Apple" in page and "No automatic update channel" in page
assert "macOS 26.6.2" in page and "Intel Macs" in page
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
assert not any(p.suffix.lower() in {".zip", ".dmg", ".pkg", ".dylib"} for p in ROOT.rglob("*"))
print("Site references, local assets and Mac release metadata OK")
