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
DETAILS = {
  "enterprise-noc-from-scratch": [
    "Infraestrutura corporativa construída do zero, com cabeamento estruturado, equipamentos Cisco, servidores Linux e monitoramento de redes.",
    "Enterprise infrastructure built from scratch, with structured cabling, Cisco networking, Linux servers and network monitoring.",
    "Cisco · Debian · Docker · Zabbix · Grafana"
  ],
  "soft-and-wet-homelab": [
    "Homelab físico de baixo consumo para explorar administração Linux, serviços self-hosted e limitações reais de hardware.",
    "Resource-efficient physical homelab for Linux administration, self-hosted services and real hardware constraints.",
    "Debian 13 · Docker Compose · Navidrome"
  ],
  "oppy": [
    "Sistema open source de monitoramento de oportunidades e envio de notificações.",
    "Open-source system for monitoring opportunities and sending notifications.",
    "Python · SQLite · Telegram"
  ],
  "usb-presence-gate": [
    "Controle de serviços Linux com base na presença física de um dispositivo USB, destinado a servidores headless.",
    "USB presence-based Linux service control for headless servers.",
    "Python · systemd · udev"
  ],
  "scrolllock-rgb-fix": [
    "Daemon leve para corrigir a iluminação RGB de teclados genéricos controlados pelo Scroll Lock no GNOME/Wayland.",
    "Lightweight daemon for generic Scroll Lock-controlled RGB keyboards on GNOME/Wayland.",
    "Python · evdev · systemd"
  ],
  "arduino-linux-controller": [
    "Controlador físico para Linux com controles multimídia, ajuste de volume, bloqueio de tela e indicadores de rede.",
    "Physical Linux controller with media controls, rotary volume, screen locking and connectivity indicators.",
    "Arduino · C++ · Python"
  ],
  "linux-networking-labs": [
    "Prática com terminal, comandos de rede e diagnóstico em Linux.",
    "Hands-on Linux terminal, networking and troubleshooting practice.",
    "Linux · CLI"
  ],
  "packet-tracer-labs": [
    "Laboratórios de topologias, switching e roteamento no Cisco Packet Tracer.",
    "Cisco Packet Tracer labs covering topology, switching and routing.",
    "Cisco · VLAN · OSPF"
  ],
  "ubuntu-server-labs": [
    "Laboratórios de administração, serviços e infraestrutura Ubuntu Server.",
    "Ubuntu Server administration, services and infrastructure labs.",
    "Ubuntu · Linux · SSH"
  ],
  "debian-server-labs": [
    "Laboratórios de administração Debian, redes, serviços e monitoramento.",
    "Debian administration, networking, services and monitoring labs.",
    "Debian · DNS · Zabbix"
  ],
  "channel-blue": [
    "Primeiro jogo 2D desenvolvido com GDevelop 5, como experiência de criação de projetos interativos.",
    "First 2D game developed with GDevelop 5 as an exploration of interactive projects.",
    "GDevelop 5 · Pixel art"
  ],
  "linux-usb-security-token": [
    "Fork voltado a documentação, testes, recuperação e salvaguardas de autenticação USB no Linux.",
    "Fork focused on documentation, testing, recovery and USB authentication safeguards on Linux.",
    "Linux · PAM · udev"
  ],
  "where-the-water-goes": [
    "Fork de um globo interativo de dados hidrológicos, com foco em compatibilidade Linux, testes e contribuições upstream.",
    "Fork of an interactive hydrological globe, focused on Linux compatibility, testing and upstream contributions.",
    "Rust · TypeScript · Tauri"
  ],
  "kayo-willian": [
    "Este espaço pessoal e o perfil público no GitHub.",
    "This personal website and public GitHub profile.",
    "HTML · CSS · Python"
  ]
}
QUOTES = [
  [
    "Johnny Joestar, Se o teu coração hesita...\n...Não atires. Ouve a mim com clareza... Se o teu coração está a hesitar, então não deves tu atirar. Pois, assim, os portões para um novo caminho se abrirão para ti.",
    "Jesus Cristo — JoJo / Steel Ball Run"
  ],
  [
    "One day I would be a better hand at the game. One day I would learn how to laugh. Pablo was waiting for me, and Mozart too...",
    "Harry Heller — O Lobo da Estepe"
  ],
  [
    "If I could just forget what happened that night - the pain, even for a second. This time, it can be different. It has to.",
    "Leon S. Kennedy — Resident Evil"
  ],
  [
    "Se o teu coração está hesitante, Não Atires. Tu crescerás... E, mais uma vez, os portões que conduzem a um 'novo caminho' se abrirão para ti.",
    "Jesus Cristo — JoJo / Steel Ball Run"
  ]
]

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
<header class="top"><a class="brand" href="{home}">GB<span>✳</span></a><a class="index-link" href="{home}#work">{tr(lang,'PROJETOS','PROJECTS')}</a><a href="{home}#index">{tr(lang,'ARQUIVO','ARCHIVE')}</a><a href="{switch}" lang="{alternate}" hreflang="{alternate}">{tr(lang,'EN','PT')}</a></header>
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
    return '<div class="work-grid">'+"".join(cards)+'</div>'

def home(lang):
    personal = [s for s in SECTIONS if s["id"] not in ("projects","existence","connection")]
    cards = "".join(f'<li><a href="{s["id"]}/"><span class="kanji" lang="ja">{e(s["ja"])}</span><span>{e(s["title"])}</span><span class="archive-arrow" aria-hidden="true">↗</span></a></li>' for s in personal)
    intro = tr(lang,"Meu trabalho gira em torno de Linux, redes, infraestrutura e software livre. Construo laboratórios e ferramentas, testo software e exploro a relação entre hardware e código.","My work revolves around Linux, networking, infrastructure and open source. I build labs and tools, test software and explore the relationship between hardware and code.")
    quotes = "".join(f'<figure class="quote"><blockquote><p>{e(q[0])}</p></blockquote><figcaption>{e(q[1])}</figcaption></figure>' for q in QUOTES)
    featured = project_grid(lang,["enterprise-noc-from-scratch","soft-and-wet-homelab","oppy","usb-presence-gate","scrolllock-rgb-fix","arduino-linux-controller"])
    labs = project_grid(lang,["linux-networking-labs","packet-tracer-labs","ubuntu-server-labs","debian-server-labs"])
    contributions = project_grid(lang,["where-the-water-goes","linux-usb-security-token"])
    other = project_grid(lang,["channel-blue","kayo-willian"])
    body = f"""<section class="hero portfolio-hero" aria-labelledby="name"><div class="hero-art">{art()}<span class="vertical" lang="ja">新しい道</span></div><div class="hero-copy"><p class="kicker">SANTARÉM / PARÁ / BRASIL</p><p class="japanese" lang="ja">ゴー・ビヨンド</p><h1 id="name">KAYO<br>WILLIAN<span>.</span></h1><p class="hero-role">GNU/Linux <span>/</span> {tr(lang,'Redes','Networking')} <span>/</span> Open Source</p><p class="intro">{e(intro)}</p><div class="hero-actions"><a class="button" href="#work">{tr(lang,'MEUS PROJETOS','MY PROJECTS')} ↓</a><a class="text-link" href="https://github.com/kayo-willian">GitHub ↗</a><a class="text-link" href="https://www.linkedin.com/in/kayo-willian">LinkedIn ↗</a></div></div><div class="hero-stamp" aria-hidden="true">GO<br>BEYOND<span>✳</span></div></section>
<section id="work" class="work-section"><div class="heading"><h2>{tr(lang,'Projetos','Projects')}<span>.</span></h2><p lang="ja">制作 / 01</p></div>{featured}</section>
<section id="labs" class="work-section"><div class="heading"><h2>{tr(lang,'Laboratórios','Labs')}<span>.</span></h2><p lang="ja">実験 / 02</p></div>{labs}</section>
<section id="oss" class="work-section"><div class="heading"><h2>Open Source<span>.</span></h2><p lang="ja">自由 / 03</p></div><p class="section-note">{tr(lang,'Forks e contribuições a projetos de terceiros, com foco em testes e documentação.','Forks and contributions to third-party projects, focused on testing and documentation.')}</p>{contributions}</section>
<section class="work-section"><div class="heading"><h2>{tr(lang,'Outros trabalhos','Other work')}<span>.</span></h2><p lang="ja">記録 / 04</p></div>{other}</section>
<section class="contact-strip" id="contact"><h2>{tr(lang,'Conexões','Connections')}<span>.</span></h2><div><a href="https://github.com/kayo-willian">GitHub ↗</a><a href="https://www.linkedin.com/in/kayo-willian">LinkedIn ↗</a><a href="https://x.com/kayowestlion">X ↗</a></div></section>
<section id="index" class="personal-archive"><div class="heading"><h2>{tr(lang,'Arquivo pessoal','Personal archive')}<span>.</span></h2><p lang="ja">記憶</p></div><p class="section-note">{tr(lang,'Algumas das coisas que gosto, leio, ouço e acompanho.','Some of the things I like, read, listen to and follow.')}</p><ul class="archive-links">{cards}</ul></section>
<section class="quotes"><div class="heading"><h2>{tr(lang,'Um novo caminho','A new path')}<span>.</span></h2><p lang="ja">新しい道</p></div>{quotes}</section>"""
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
