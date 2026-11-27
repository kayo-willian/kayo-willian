#!/usr/bin/env python3
"""Build a minimal bilingual foundation without external dependencies."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
CATALOG = json.loads((ROOT / "content" / "catalog.json").read_text(encoding="utf-8"))

def esc(value):
    return html.escape(str(value), quote=True)

def render(lang):
    pt = lang == "pt"
    locale = "pt-BR" if pt else "en"
    other = "en/" if pt else "../"
    css = "style.css" if pt else "../style.css"
    title = "Arquivo pessoal em construção" if pt else "Personal archive under construction"
    nav = "Índice editorial" if pt else "Editorial index"
    intro = "Tecnologia, cultura e experimentação. A fundação do site está em desenvolvimento." if pt else "Technology, culture and experimentation. The site's foundation is under development."
    cards = "".join(
        f'<li><span lang="ja">{esc(s["ja"])}</span><h3>{esc(s["title"])}</h3><p>{esc(s["description"][lang])}</p></li>'
        for s in CATALOG["sections"]
    )
    return f"""<!doctype html>
<html lang="{locale}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="robots" content="noindex">
<title>GO BEYOND — {esc(title)}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<header><a href="{other}" hreflang="{'en' if pt else 'pt-BR'}" lang="{'en' if pt else 'pt-BR'}">{'English' if pt else 'Português'}</a></header>
<main>
<section class="hero" aria-labelledby="title">
<p class="eyebrow" lang="ja">ゴー・ビヨンド</p>
<h1 id="title">GO<br>BEYOND<span>.</span></h1>
<p class="intro">{esc(intro)}</p>
</section>
<section aria-labelledby="index">
<h2 id="index">{esc(nav)}</h2>
<ul class="grid">{cards}</ul>
</section>
</main>
<footer><a href="https://github.com/kayo-willian">GitHub</a> / FOUNDATION</footer>
</body>
</html>"""

def main():
    assert len(CATALOG["sections"]) == 19
    assert len({s["id"] for s in CATALOG["sections"]}) == 19
    assert len(CATALOG["fighters"]) == 18
    assert len(CATALOG["homeQuotes"]) == 4
    assert all(s["description"].get("pt") and s["description"].get("en") for s in CATALOG["sections"])
    OUT.mkdir(exist_ok=True)
    (OUT / "en").mkdir(exist_ok=True)
    (OUT / "index.html").write_text(render("pt"), encoding="utf-8")
    (OUT / "en" / "index.html").write_text(render("en"), encoding="utf-8")
    (OUT / "style.css").write_text((ROOT / "src" / "style.css").read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print("Built and validated 19 sections, 18 fighters and 4 homepage quote slots.")

if __name__ == "__main__":
    main()
