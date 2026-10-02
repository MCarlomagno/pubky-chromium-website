"""Check local site references and the pending-download contract."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / "docs"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values.get("href", ""))
        if tag in ("img", "script", "link"):
            ref = values.get("src") or values.get("href")
            if ref:
                self.images.append(ref)


page = (ROOT / "index.html").read_text()
references = References()
references.feed(page)
assert (ROOT / "style.css").is_file()
assert "Download not available yet" in page
assert "https://github.com/MCarlomagno/pubky-chromium" in references.links
assert not any("download" in link.lower() or "releases/" in link for link in references.links)
assert references.images and all(not urlsplit(ref).scheme for ref in references.images)
for ref in references.links + references.images:
    url = urlsplit(ref)
    if url.scheme:
        assert url.scheme == "https", ref
        continue
    assert ref and not ref.startswith("/") and ".." not in Path(url.path).parts, ref
    assert (ROOT / url.path).is_file(), ref
print("Site references and pending-download state OK")
