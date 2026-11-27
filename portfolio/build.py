#!/usr/bin/env python3
"""Generate the bilingual personal archive."""
import html
import json
import shutil
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
CAT = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))["projects"]
SECTIONS = CAT["sections"]
DETAILS = json.loads((ROOT / "content/project-details.json").read_text(encoding="utf-8"))
QUOTES = json.loads((ROOT / "content/quotes.json").read_text(encoding="utf-8"))

def e(value):
    return html.escape(str(value), quote=True)

def tr(lang, pt, en):
    return pt if lang == "pt" else en

def page(lang, title, body, section=None):
    home = "../" if section else "./"
    css = ("../" if lang == "pt" else "") + home + "style.css"
    switch = ("../../" if section else "../") if lang == "pt" else ("../pt-br/" if section else "pt-br/")
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
<header class="top"><a class="brand" href="{home}">GO <span>BEYOND</span><small lang="ja">ゴー・ビヨンド</small></a><a class="index-link" href="{home}#work">{tr(lang,'PROJETOS','PROJECTS')}</a><a href="{home}#index">{tr(lang,'ARQUIVO','ARCHIVE')}</a><a class="language" href="{switch}" lang="{alternate}" hreflang="{alternate}">{tr(lang,'EN','PT-BR')}</a></header>
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

def project_grid(lang, slugs):
    cards = []
    for slug in slugs:
        project = next(p for p in PROJECTS if p[0] == slug)
        _, title, pt, en = project
        desc_pt, desc_en, tech = DETAILS[slug]
        label = tr(lang,pt,en)
        if slug in ("linux-usb-security-token","where-the-water-goes"):
            label = tr(lang,"Fork / contribuição","Fork / contribution")
        cards.append(f'<article class="work-card"><p class="work-kind">{e(label)}</p><h3>{e(title)}</h3><p class="work-description">{e(tr(lang,desc_pt,desc_en))}</p><p class="work-tech">{e(tech)}</p><a class="work-link" href="https://github.com/kayo-willian/{e(slug)}">GitHub ↗<span class="sr-only"> — {e(title)}</span></a></article>')
    return '<div class="work-grid '+('six' if len(cards)==6 else 'even')+'">'+ "".join(cards)+'</div>'

def quote(lang, index, theme):
    q = QUOTES[index]
    note = tr(lang,"Tradução inglesa do texto fornecido","English rendering of the supplied text") if q.get("translation") else ""
    return f'<figure class="quote-band"><div class="quote-marker"><span lang="ja">言葉</span><small>{e(theme)}</small></div><div><blockquote lang="en"><p>“{e(q["body"])}”</p></blockquote><figcaption>{e(q["by"])} — {e(q["work"])}{f" · {e(note)}" if note else ""}</figcaption></div></figure>'

def home(lang):
    personal = [s for s in SECTIONS if s["id"] not in ("projects","existence","connection")]
    cards = "".join(f'<li><a href="{s["id"]}/"><span class="kanji" lang="ja">{e(s["ja"])}</span><span>{e(s["title"])}</span><span class="archive-arrow" aria-hidden="true">↗</span></a></li>' for s in personal)
    intro = tr(lang,"Meu trabalho gira em torno de Linux, redes, infraestrutura e software livre. Construo laboratórios e ferramentas, testo software e exploro a relação entre hardware e código.","My work revolves around Linux, networking, infrastructure and open source. I build labs and tools, test software and explore the relationship between hardware and code.")
    featured = project_grid(lang,["enterprise-noc-from-scratch","soft-and-wet-homelab","oppy","usb-presence-gate","scrolllock-rgb-fix","arduino-linux-controller"])
    labs = project_grid(lang,["linux-networking-labs","packet-tracer-labs","ubuntu-server-labs","debian-server-labs"])
    contributions = project_grid(lang,["where-the-water-goes","linux-usb-security-token"])
    other = project_grid(lang,["channel-blue","kayo-willian"])
    image = ("../" if lang == "pt" else "") + "images/header-blue.jpg"
    body = f"""<section class="hero portfolio-hero" aria-labelledby="name"><div class="hero-art">{art()}<span class="vertical" lang="ja">新しい道</span></div><div class="hero-copy"><p class="kicker">SANTARÉM / PARÁ / {tr(lang,'BRASIL','BRAZIL')}</p><p class="japanese" lang="ja">ゴー・ビヨンド</p><h1 id="name">KAYO<br>WILLIAN<span>.</span></h1><p class="hero-role">GNU/Linux <span>/</span> {tr(lang,'Redes','Networking')} <span>/</span> Open Source</p><p class="intro">{e(intro)}</p><div class="hero-actions"><a class="button" href="#work">{tr(lang,'MEUS PROJETOS','MY PROJECTS')} ↓</a><a class="text-link" href="https://github.com/kayo-willian">GitHub ↗</a><a class="text-link" href="https://www.linkedin.com/in/kayo-willian">LinkedIn ↗</a><a class="text-link" href="https://x.com/kayowestlion">X ↗</a></div></div><div class="hero-stamp" aria-hidden="true">GO<br>BEYOND<span>✳</span></div></section>
{quote(lang,0,tr(lang,'UM NOVO CAMINHO','A NEW PATH'))}
<section class="profile-panel" aria-labelledby="profile"><div><p class="kicker" lang="ja">存在 / EXISTENCE</p><h2 id="profile">{tr(lang,'Além do código','Beyond the code')}<span>.</span></h2><p>{tr(lang,'Tenho interesse por sistemas, máquinas e pelo desconhecido. Aprender, testar e construir são formas de explorar essas coisas.','I am drawn to systems, machines and the unknown. Learning, testing and building are ways of exploring them.')}</p></div><div class="terminal"><div class="terminal-top"><span></span><span></span><span></span><small>profile.yaml</small></div><div class="terminal-body"><p><b>$</b> cat profile.yaml</p><dl><dt>ecosystem</dt><dd>GNU/Linux</dd><dt>philosophy</dt><dd>Open Source</dd><dt>interests</dt><dd>Hardware &amp; Software</dd><dt>activities</dt><dd>Testing, Research &amp; Development</dd><dt>curiosity</dt><dd>The Unknown</dd></dl></div></div></section>
<section id="work" class="work-section"><div class="heading"><h2>{tr(lang,'Projetos','Projects')}<span>.</span></h2><p lang="ja">制作 / 01</p></div>{featured}</section>
<section id="labs" class="work-section"><div class="heading"><h2>{tr(lang,'Laboratórios','Labs')}<span>.</span></h2><p lang="ja">実験 / 02</p></div>{labs}</section>
{quote(lang,1,tr(lang,'APRENDER','LEARNING'))}
<section id="oss" class="work-section"><div class="heading"><h2>{tr(lang,'Contribuições open source','Open source contributions')}<span>.</span></h2><p lang="ja">自由 / 03</p></div><p class="section-note">{tr(lang,'Forks e contribuições a projetos de terceiros, com foco em testes e documentação.','Forks and contributions to third-party projects, focused on testing and documentation.')}</p>{contributions}</section>
<section class="work-section"><div class="heading"><h2>{tr(lang,'Outros trabalhos','Other work')}<span>.</span></h2><p lang="ja">記録 / 04</p></div>{other}</section>
{quote(lang,2,tr(lang,'TENTAR NOVAMENTE','TRYING AGAIN'))}
<section class="contact-strip" id="contact"><h2>{tr(lang,'Conexões','Connections')}<span>.</span></h2><div><a href="https://github.com/kayo-willian">GitHub ↗</a><a href="https://www.linkedin.com/in/kayo-willian">LinkedIn ↗</a><a href="https://x.com/kayowestlion">X ↗</a><a href="mailto:kayowillian.net@protonmail.com">{tr(lang,'E-mail','Email')} ↗</a></div></section>
<section id="index" class="personal-archive"><div class="heading"><h2>{tr(lang,'Arquivo pessoal','Personal archive')}<span>.</span></h2><p lang="ja">記憶</p></div><p class="section-note">{tr(lang,'As coisas que leio, ouço, acompanho e revisito.','The things I read, listen to, follow and return to.')}</p><div class="underground-banner"><img src="{image}" alt="{tr(lang,'Arte do espadachim do Tsurugi Linux','Tsurugi Linux swordsman artwork')}" loading="lazy"><div><p class="kicker" lang="ja">地下 / UNDERGROUND</p><a href="underground/">TSURUGI <span>↗</span></a><p>{tr(lang,'Linux, OSINT e cultura hacker','Linux, OSINT and hacker culture')}</p></div></div><ul class="archive-links">{cards}</ul></section>
{quote(lang,3,'GO BEYOND')}"""
    return page(lang,"Kayo Willian — GO BEYOND",body)

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
        return project_grid(lang,[p[0] for p in PROJECTS])
    if sid == "sound": return list_items(CAT["music"]["artists"] + CAT["music"]["goats"])
    if sid == "goats": return '<div class="goat-pair"><p>MICHAEL<br>JACKSON</p><p>KANYE<br>WEST</p></div>'
    if sid == "fight":
        return '<ul class="fighters">' + "".join(f'<li class="{"featured" if f["featured"] else ""}"><small>{e(f["name"])}</small><strong>{e(f["label"])}</strong><span>{e(f["sport"].upper())}</span></li>' for f in CAT["fighters"]) + '</ul>'
    if sid == "seinen": return list_items(CAT["seinen"])
    if sid == "heretics": return list_items([x.split(" / ")[1 if lang=="en" else 0] if " / " in x else x for x in CAT["comics"]])
    if sid == "library": return library(lang)
    if sid == "games": return list_items(CAT["games"])
    if sid == "underground": return list_items(CAT["screen"] + ["Tsurugi Linux","GNU/Linux","Unix",tr(lang,"Internet independente","Independent web")])
    if sid == "freedom": return list_items(["GNU/Linux","Open Source",tr(lang,"Software livre","Free software")])
    if sid == "origins": return list_items([tr(lang,"Brasil","Brazil"),tr(lang,"Amazônia","Amazon"),"Santarém — Pará"])
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
        if tag == "img" and "src" in a: self.links.append(a["src"])

def validate():
    assert len(SECTIONS) == len({s["id"] for s in SECTIONS}) == 19
    assert len(CAT["fighters"]) == 18
    assert len(CAT["homeQuotes"]) == len(QUOTES) == 4
    assert set(DETAILS) == {p[0] for p in PROJECTS}
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
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(exist_ok=True)
    (OUT / "images").mkdir()
    shutil.copyfile(ROOT.parent / "assets/header-blue.jpg", OUT / "images/header-blue.jpg")
    for lang in ("en","pt"):
        root = OUT if lang == "en" else OUT / "pt-br"
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
