"""Shared page furniture and repository-relative navigation."""
from html import escape
from pathlib import Path
import json
import posixpath

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kayo-willian.github.io/kayo-willian/'
PROFILE = 'https://github.com/kayo-willian'
SOCIAL = [('GitHub', PROFILE), ('LinkedIn', 'https://www.linkedin.com/in/kayo-willian'), ('X', 'https://x.com/kayowestlion'), ('email', 'mailto:kayowillian.net@protonmail.com')]


def data(name):
    return json.loads((ROOT / 'content' / (name + '.json')).read_text(encoding='utf-8'))


def e(value):
    return escape(str(value), quote=True)


def icon(name):
    shapes = {'external': 'M5 13 13 5M5 5h8v8', 'right': 'M2 9h13m-5-5 5 5-5 5', 'down': 'M9 2v13m-5-5 5 5 5-5', 'up': 'M9 16V3m-5 5 5-5 5 5', 'plus': 'M3 9h12M9 3v12', 'menu': 'M2 5h14M2 12h14', 'chevron': 'm3 7 6 6 6-6'}
    return f'<svg class="icon" aria-hidden="true" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6"><path d="{shapes[name]}"/></svg>'


def link(url, label, glyph='external', css='inline-link'):
    return f'<a class="{css}" href="{e(url)}">{e(label)} {icon(glyph)}</a>'


def mark():
    return '<svg class="mark" viewBox="0 0 42 30" aria-hidden="true" fill="currentColor"><path d="M0 27 15 3h8L8 27zm15 0L30 3h8L23 27z"/><path d="M27 27 38 9l3 5-8 13z"/></svg>'


def social(t):
    return ''.join(link(url, t.get(label, label)) for label, url in SOCIAL)


def route(lang, slug=None):
    return ('pt-br/' if lang == 'pt' else '') + (f'projects/{slug}/' if slug else '')


class Page:
    def __init__(self, lang, assets, slug=None):
        self.lang = lang
        self.t = data('interface')[lang]
        self.path = route(lang, slug)
        self.slug = slug
        self.assets = assets

    def url(self, target):
        address, sep, fragment = target.partition('#')
        relative = posixpath.relpath(address or '.', self.path or '.')
        if relative == '.' and sep:
            return '#' + fragment
        if address.endswith('/') or not address:
            relative += '/'
        return relative + sep + fragment

    def asset(self, file):
        return self.url(self.assets[file])

    def home(self, fragment=''):
        return self.url(route(self.lang) + fragment)

    def project(self, slug):
        return self.url(route(self.lang, slug))

    def document(self, title, body, description):
        t = self.t
        lang, alt = ('pt-BR', 'en') if self.lang == 'pt' else ('en', 'pt-BR')
        target = route('en' if self.lang == 'pt' else 'pt', self.slug)
        links = ''.join(f'<a href="{self.home("#" + key)}">{e(t[label])}</a>' for key, label in [('work','projects'),('labs','labs'),('oss','open'),('security','security')])
        return f'''
<!doctype html>

<html lang="{lang}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="robots" content="noindex">
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#050608">
    <meta name="description" content="{e(description)}"><title>{e(title)} · GO BEYOND</title>
    <link rel="canonical" href="{BASE}{self.path}">
    <link rel="alternate" hreflang="{alt}" href="{BASE}{target}">
    <link rel="icon" href="{self.asset('art/mark.svg')}" type="image/svg+xml">
    <link rel="stylesheet" href="{self.asset('style.css')}">
    <script defer src="{self.asset('nav.js')}"></script>
  </head>

  <body id="top"><a class="skip" href="#main">{t['skip']}</a>

    <header class="header frame"><a class="wordmark" aria-label="{t['brandHome']}" href="{self.home()}">GO BEYOND</a>
      <nav id="nav" aria-label="{t['portfolio']}">{links}
      </nav><a class="language" href="{self.url(target)}" lang="{alt}" hreflang="{alt}" aria-label="{t['language']}"><span class="lang-dot"></span>{alt.upper()}</a><button type="button" class="menu" aria-controls="nav" aria-expanded="false">{t['menu']} {icon('menu')}</button>
    </header>

    <main id="main">{body}
    </main>
    <footer class="footer frame"><span>{t['footerLine']}</span>
      <div>{link(PROFILE+'/kayo-willian', t['source'])}{link('#top',t['back'],'up')}
      </div>
    </footer>
  </body>
</html>
'''
