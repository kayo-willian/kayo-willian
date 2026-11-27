#!/usr/bin/env python3
"""Generate the bilingual technical portfolio."""
import html
import json
import shutil
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
PROJECTS = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))["projects"]
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
<header class="top"><a class="brand" href="{home}">GO <span>BEYOND</span></a><a class="index-link" href="{home}#work">{tr(lang,'PROJETOS','PROJECTS')}</a><a href="{home}#oss">OPEN SOURCE</a><a href="{home}#security">{tr(lang,'SEGURANÇA','SECURITY')}</a><a class="language" href="{switch}" lang="{alternate}" hreflang="{alternate}">{tr(lang,'EN','PT-BR')}</a></header>
<main id="main">{body}</main>
<footer><span>GO BEYOND / KAYO WILLIAN</span><a href="https://github.com/kayo-willian">GITHUB ↗</a><a href="{home}#main">{tr(lang,'VOLTAR AO TOPO','BACK TO TOP')} ↑</a></footer>
</body></html>"""

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
    note = tr(lang,"Tradução inglesa do texto fornecido","English rendering of the supplied text")
    return f'<figure class="quote-band"><div class="quote-marker"><small>{e(theme)}</small></div><div><blockquote lang="en"><p>“{e(q["body"])}”</p></blockquote><figcaption>{e(q["by"])} — {e(q["work"])} · {e(note)}</figcaption></div></figure>'

def home(lang):
    intro = tr(lang,"Exploro sistemas Linux, redes e infraestrutura. Construo ferramentas e laboratórios, testo software e documento o que aprendo.","I explore Linux systems, networking and infrastructure. I build tools and labs, test software and document what I learn.")
    featured = project_grid(lang,["enterprise-noc-from-scratch","soft-and-wet-homelab","oppy","usb-presence-gate","scrolllock-rgb-fix","arduino-linux-controller"])
    labs = project_grid(lang,["linux-networking-labs","packet-tracer-labs","ubuntu-server-labs","debian-server-labs"])
    contributions = project_grid(lang,["where-the-water-goes","linux-usb-security-token"])
    other = project_grid(lang,["channel-blue","kayo-willian"])
    body = f"""<section class="hero portfolio-hero" aria-labelledby="name"><div class="hero-copy"><p class="japanese" lang="ja">ゴー・ビヨンド</p><h1 id="name">KAYO<br>WILLIAN<span>.</span></h1><p class="hero-role">GNU/Linux <span>/</span> {tr(lang,'Redes','Networking')} <span>/</span> Open Source</p><p class="intro">{e(intro)}</p><div class="hero-actions"><a class="button" href="#work">{tr(lang,'MEUS PROJETOS','MY PROJECTS')} ↓</a><a class="text-link" href="https://github.com/kayo-willian">GitHub ↗</a><a class="text-link" href="https://www.linkedin.com/in/kayo-willian">LinkedIn ↗</a><a class="text-link" href="https://x.com/kayowestlion">X ↗</a></div></div><div class="hero-symbol"><span class="ocean-kanji" lang="ja" aria-label="{tr(lang,'Mar','Sea')}">海</span><span class="symbol-caption">{tr(lang,'MAR','SEA')} / GO BEYOND</span></div></section>
{quote(lang,0,tr(lang,'UM NOVO CAMINHO','A NEW PATH'))}
<section class="profile-panel" aria-labelledby="profile"><div><p class="kicker">{tr(lang,'PERFIL TÉCNICO','TECHNICAL PROFILE')}</p><h2 id="profile">{tr(lang,'Áreas de atuação','Technical focus')}<span>.</span></h2><p>{tr(lang,'Administração Linux, redes, infraestrutura, automação e testes de software.','Linux administration, networking, infrastructure, automation and software testing.')}</p></div><div class="terminal"><div class="terminal-top"><span></span><span></span><span></span><small>profile.yaml</small></div><div class="terminal-body"><p><b>$</b> cat profile.yaml</p><dl><dt>ecosystem</dt><dd>GNU/Linux</dd><dt>philosophy</dt><dd>Open Source</dd><dt>focus</dt><dd>{tr(lang,'Redes e infraestrutura','Networking &amp; Infrastructure')}</dd><dt>activities</dt><dd>{tr(lang,'Testes e desenvolvimento','Testing &amp; Development')}</dd></dl></div></div></section>
<section id="work" class="work-section"><div class="heading"><h2>{tr(lang,'Projetos','Projects')}<span>.</span></h2><p>01</p></div>{featured}</section>
<section id="labs" class="work-section"><div class="heading"><h2>{tr(lang,'Laboratórios','Labs')}<span>.</span></h2><p>02</p></div>{labs}</section>
<section id="oss" class="work-section"><div class="heading"><h2>{tr(lang,'Contribuições open source','Open source contributions')}<span>.</span></h2><p>03</p></div><p class="section-note">{tr(lang,'Forks e contribuições a projetos de terceiros, com foco em testes e documentação.','Forks and contributions to third-party projects, focused on testing and documentation.')}</p>{contributions}</section>
<section id="security" class="work-section security-section"><div class="heading"><h2>{tr(lang,'Cibersegurança','Cybersecurity')}<span>.</span></h2><p>04</p></div><p class="section-note">{tr(lang,'Área de estudo: defesa de redes, segurança de sistemas Linux e monitoramento.','Learning focus: network defense, Linux system security and monitoring.')}</p><ul class="security-topics"><li>{tr(lang,'Defesa de redes','Network defense')}</li><li>{tr(lang,'Segurança Linux','Linux security')}</li><li>{tr(lang,'Monitoramento','Monitoring')}</li></ul></section>
<section class="work-section"><div class="heading"><h2>{tr(lang,'Outros projetos','Other projects')}<span>.</span></h2><p>05</p></div>{other}</section>
<section class="contact-strip" id="contact"><h2>{tr(lang,'Contato','Contact')}<span>.</span></h2><div><a href="https://github.com/kayo-willian">GitHub ↗</a><a href="https://www.linkedin.com/in/kayo-willian">LinkedIn ↗</a><a href="https://x.com/kayowestlion">X ↗</a><a href="mailto:kayowillian.net@protonmail.com">{tr(lang,'E-mail','Email')} ↗</a></div></section>
{quote(lang,1,'GO BEYOND')}
<div class="closing-mark"><span lang="ja">海</span><span>GO BEYOND.</span></div>"""
    return page(lang,"Kayo Willian — GO BEYOND",body)

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
    assert len(QUOTES) == 2 and all(q["by"]=="Jesus Christ" for q in QUOTES)
    assert set(DETAILS) == {p[0] for p in PROJECTS}
    pages = list(OUT.rglob("*.html"))
    assert len(pages) == 2
    for path in pages:
        text = path.read_text(encoding="utf-8")
        assert all(x not in text for x in ("Personal archive","Arquivo pessoal","Tsurugi","Steppenwolf","Resident Evil","SANTARÉM"))
        assert text.count("<blockquote") == 2
        p = LinkParser()
        p.feed(text)
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
    print("Validated two localized portfolio pages and all internal links.")

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(exist_ok=True)
    for lang in ("en","pt"):
        root = OUT if lang == "en" else OUT / "pt-br"
        root.mkdir(exist_ok=True)
        (root / "index.html").write_text(home(lang),encoding="utf-8")
    (OUT / "style.css").write_text((ROOT / "src/style.css").read_text(encoding="utf-8"),encoding="utf-8")
    (OUT / ".nojekyll").touch()
    validate()

if __name__ == "__main__":
    main()
