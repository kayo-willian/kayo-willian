#!/usr/bin/env python3
"""Check the generated Astro output and internal links."""
import sys
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
BASE = "/kayo-willian/"
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.lang = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if "id" in a: self.ids.add(a["id"])
        if tag in ("a","link") and "href" in a: self.links.append(a["href"])
        if tag == "img" and "src" in a: self.links.append(a["src"])
def parse(path):
    p = Parser()
    p.feed(path.read_text(encoding="utf-8"))
    return p
def validate():
    pages = list(OUT.rglob("*.html"))
    assert len(pages) >= 40, len(pages)
    assert parse(OUT/"index.html").lang == "en"
    assert parse(OUT/"pt-br/index.html").lang == "pt-BR"
    assert (OUT/"images/header-blue.jpg").is_file()
    for path in pages:
        p = parse(path)
        for link in p.links:
            u = urlsplit(link)
            if u.scheme or u.netloc: continue
            if u.path.startswith(BASE): dest = OUT / unquote(u.path[len(BASE):])
            elif u.path.startswith("/"): dest = OUT / unquote(u.path.lstrip("/"))
            elif u.path: dest = path.parent / unquote(u.path)
            else: dest = path
            if dest.is_dir(): dest = dest/"index.html"
            assert dest.is_file(), (path,link)
            if u.fragment and dest.suffix == ".html":
                assert unquote(u.fragment) in parse(dest).ids, (path,link)
    print(f"Validated {len(pages)} pages, local assets and internal links.")
if __name__ == "__main__":
    if "--check" not in sys.argv:
        subprocess.run(["npm","run","build"],cwd=ROOT,check=True)
    validate()
