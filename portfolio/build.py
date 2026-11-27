#!/usr/bin/env python3
"""Generate the bilingual personal archive."""
import html
import json
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
CAT = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))["projects"]
SECTIONS = CAT["sections"]

def e(value):
    return html.escape(str(value), quote=True)

def tr(lang, pt, en):
    return pt if lang == "pt" else en

def page(lang, title, body, section=None):
    home = "../" if section else "./"
    css = ("../" if lang == "en" else "") + home + "style.css"
    switch = ("../../" if section else "../") if lang == "en" else ("../en/" if section else "en/")
    if section:
        switch += section + "/"
    locale = tr(lang, "pt-BR", "en")
    alternate = tr(lang, "en", "pt-BR")
    return f"""<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="robots" content="noindex">
<title>{e(title)} | GO BEYOND</title>
<link rel="stylesheet" href="{css}"></head>
<body class="{e(section or 'home')}">
<a class="skip" href="#main">{tr(lang,'Ir ao conteúdo','Skip to content')}</a>
<header class="top"><a class="brand" href="{home}">GB<span>✳</span></a><a class="index-link" href="{home}#index">{tr(lang,'ÍNDICE','INDEX')}</a><a href="{switch}" lang="{alternate}" hreflang="{alternate}">{tr(lang,'EN','PT')}</a></header>
<main id="main">{body}</main>
<footer><span>GO BEYOND / KAYO WILLIAN</span><a href="https://github.com/kayo-willian">GITHUB ↗</a><a href="{home}#index">{tr(lang,'ÍNDICE','INDEX')} ↑</a></footer>
</body></html>"""

def art():
    return """<svg class="orbit" viewBox="0 0 480 480" aria-hidden="true" focusable="false">
<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="currentColor" stroke-opacity=".15"/></pattern></defs>
<circle cx="240" cy="240" r="223" fill="url(#grid)" stroke="currentColor" stroke-width="1"/>
<g fill="none" stroke="currentColor"><circle cx="240" cy="240" r="169"/><circle cx="240" cy="240" r="102"/><ellipse cx="240" cy="240" rx="222" ry="75" transform="rotate(-35 240 240)"/><ellipse cx="240" cy="240" rx="222" ry="75" transform="rotate(55 240 240)"/><path d="M17 240H463M240 17V463" stroke-dasharray="4 8"/></g>
<circle cx="240" cy="240" r="17" fill="currentColor"/><circle cx="359" cy="121" r="8" fill="currentColor"/><circle cx="89" cy="303" r="5" fill="currentColor"/>
</svg>"""

def home(lang):
    cards = "".join(f'<li><a href="{s["id"]}/"><span class="num">{i:02}</span><span class="kanji" lang="ja">{e(s["ja"])}</span><h3>{e(s["title"])}</h3><p>{e(s["description"][lang])}</p><span class="arrow" aria-hidden="true">↗</span></a></li>' for i,s in enumerate(SECTIONS,1))
    intro = tr(lang,"Um espaço pessoal na internet. Tecnologia, música, lutas, literatura e tudo o que existe entre essas coisas.","A personal space on the internet. Technology, music, fighting, literature and everything in between.")
    # Full supplied quotations are held back until the source/rights review.
    quotes = "".join(f'<div class="quote-slot"><span class="num">0{i}</span><cite>{e(q["speaker"])} — {e(q["source"])}</cite></div>' for i,q in enumerate(CAT["homeQuotes"],1))
    body = f"""<section class="hero"><div class="hero-art">{art()}<span class="vertical" lang="ja">新しい道</span></div><div class="hero-copy"><p class="kicker">BRASIL / AMAZÔNIA / 2026</p><p class="japanese" lang="ja">ゴー・ビヨンド</p><h1>GO<br>BEYOND<span>.</span></h1><p class="owner">KAYO WILLIAN</p><p class="intro">{intro}</p><a class="button" href="#index">{tr(lang,'EXPLORAR','EXPLORE')} ↓</a></div></section>
<section id="index" class="archive"><div class="heading"><h2>{tr(lang,'Índice','Index')}<span>.</span></h2><p>19 / {tr(lang,'ESPAÇOS','SPACES')}</p></div><ul class="grid">{cards}</ul></section>
<section class="quotes"><h2>{tr(lang,'Um novo caminho','A new path')}<span>.</span></h2>{quotes}</section>"""
    return page(lang,"GO BEYOND",body)

def list_items(items):
    return '<ul class="names">' + "".join(f'<li>{e(item)}</li>' for item in items) + '</ul>'

def links(lang, entries):
    return '<ul class="names">' + "".join(f'<li><a href="{e(url)}">{e(label)} ↗</a></li>' for label,url in entries) + '</ul>'

def library(lang):
    ranking = '<ol class="ranking">' + "".join(f'<li>{e(title)}</li>' for title in CAT["library"]["ranking"]) + '</ol>'
    labels = {"read":tr(lang,"Lido","Read"),"abandoned":tr(lang,"Abandonado","Abandoned"),"uncertain":tr(lang,"Talvez","Maybe"),"unspecified":tr(lang,"Não informado","Unspecified")}
    rows = "".join(f'<tr><th scope="row">{e(b["title"])}</th><td>{e(b["author"])}</td><td>{e(labels[b["status"]])}</td><td>{e(str(b["rating"])+"/10" if b["rating"] is not None else "—")}</td></tr>' for b in CAT["library"]["books"])
    headers = [tr(lang,"Livro","Book"),tr(lang,"Autor","Author"),tr(lang,"Estado","Status"),tr(lang,"Nota","Rating")]
    return f'<h2>TOP 05</h2>{ranking}<div class="table-wrap"><table><thead><tr>{"".join(f"<th scope=col>{e(x)}</th>" for x in headers)}</tr></thead><tbody>{rows}</tbody></table></div>'

def content(lang, sid):
    if sid == "projects":
        return '<ul class="names projects-list">' + "".join(f'<li><a href="https://github.com/kayo-willian/{e(slug)}"><small>{e(tr(lang,pt,en))}</small>{e(title)} <span>↗</span></a></li>' for slug,title,pt,en in PROJECTS) + '</ul>'
    if sid == "sound": return list_items(CAT["music"]["artists"] + CAT["music"]["goats"])
    if sid == "goats": return '<div class="goat-pair"><p>MICHAEL<br>JACKSON</p><p>KANYE<br>WEST</p></div>'
    if sid == "fight":
        return '<ul class="fighters">' + "".join(f'<li class="{"featured" if f["featured"] else ""}"><small>{e(f["name"])}</small><strong>{e(f["label"])}</strong><span>{e(f["sport"].upper())}</span></li>' for f in CAT["fighters"]) + '</ul>'
    if sid == "seinen": return list_items(CAT["seinen"])
    if sid == "heretics": return list_items(CAT["comics"])
    if sid == "library": return library(lang)
    if sid == "games": return list_items(CAT["games"])
    if sid == "underground": return list_items(CAT["screen"] + ["GNU/Linux","Unix",tr(lang,"Internet independente","Independent web")])
    if sid == "freedom": return list_items(["GNU/Linux","Open Source",tr(lang,"Software livre","Free software")])
    if sid == "origins": return list_items(["Brasil","Amazônia","Santarém — Pará"])
    if sid == "earth": return list_items([tr(lang,"Rios amazônicos","Amazon rivers"),tr(lang,"Florestas","Forests"),tr(lang,"Geografia","Geography")])
    if sid == "machines": return list_items(["GNU/Linux","Hardware",tr(lang,"Servidores","Servers"),tr(lang,"Máquinas imaginárias","Imaginary machines")])
    if sid == "aesthetics": return list_items([tr(lang,"Tipografia japonesa","Japanese typography"),tr(lang,"Arte analógica e digital","Analog and digital art"),"Manga","Afrofuturism"])
    if sid == "black-culture": return list_items([tr(lang,"Cultura negra","Black culture"),tr(lang,"Música","Music"),tr(lang,"Afrofuturismo","Afrofuturism")])
    if sid == "connection": return links(lang,[("GitHub","https://github.com/kayo-willian"),("LinkedIn","https://www.linkedin.com/in/kayo-willian"),("X","https://x.com/kayowestlion")])
    if sid == "existence": return '<p class="lead">Kayo Willian — GNU/Linux, Open Source, Hardware &amp; Software.</p>'
    if sid == "experiments": return '<div class="experiment-art">'+art()+'</div>'
    return '<p class="lead">'+tr(lang,"Arquivo em construção.","Archive in development.")+'</p>'

def section_page(lang,s,index):
    body = f'<section class="section-head"><p class="kicker">ARCHIVE / {index:02}</p><p class="japanese" lang="ja">{e(s["ja"])}</p><h1>{e(s["title"])}<span>.</span></h1><p class="intro">{e(s["description"][lang])}</p></section><section class="section-body">{content(lang,s["id"])}</section>'
    return page(lang,s["title"],body,s["id"])

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag in ("a","link") and "href" in a: self.links.append(a["href"])

def validate():
    assert len(SECTIONS) == len({s["id"] for s in SECTIONS}) == 19
    assert len(CAT["fighters"]) == 18
    assert len(CAT["homeQuotes"]) == 4
    assert len(PROJECTS) == len({p[0] for p in PROJECTS}) == 14
    pages = list(OUT.rglob("*.html"))
    assert len(pages) == 40
    for path in pages:
        p = LinkParser()
        p.feed(path.read_text(encoding="utf-8"))
        for link in p.links:
            if link.startswith(("https://","http://","mailto:")): continue
            target, _, fragment = link.partition("#")
            dest = path.parent / target if target else path
            if dest.is_dir(): dest = dest / "index.html"
            assert dest.is_file(), (path,link)
            if fragment:
                q = LinkParser()
                q.feed(dest.read_text(encoding="utf-8"))
                assert fragment in q.ids,(path,link)
    print("Validated 40 HTML pages and all internal links.")

def main():
    OUT.mkdir(exist_ok=True)
    for lang in ("pt","en"):
        root = OUT if lang == "pt" else OUT / "en"
        root.mkdir(exist_ok=True)
        (root / "index.html").write_text(home(lang),encoding="utf-8")
        for index,s in enumerate(SECTIONS,1):
            directory = root / s["id"]
            directory.mkdir(exist_ok=True)
            (directory / "index.html").write_text(section_page(lang,s,index),encoding="utf-8")
    (OUT / "style.css").write_text((ROOT / "src/style.css").read_text(encoding="utf-8"),encoding="utf-8")
    (OUT / ".nojekyll").touch()
    validate()

if __name__ == "__main__":
    main()
