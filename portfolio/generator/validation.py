"""Check the published tree, including cross-page anchors and CSS asset paths."""
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.lang = ''
        self.h1 = 0
        self.quotes = 0
        self.japanese = 0
        self.feed(source)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if ident := attrs.get('id'):
            if ident in self.ids:
                raise ValueError(f'Duplicate id: {ident}')
            self.ids.add(ident)
        if tag == 'html':
            self.lang = attrs.get('lang')
        self.h1 += int(tag == 'h1')
        self.quotes += int(tag == 'blockquote')
        self.japanese += int(attrs.get('lang') == 'ja')
        if tag == 'img' and 'alt' not in attrs:
            raise ValueError('Missing image alt attribute')
        for key in ['src', 'href']:
            if key in attrs:
                self.refs.append(attrs[key])


def verify(out, project_ids):
    docs = {path: Document(path.read_text(encoding='utf-8')) for path in out.rglob('*.html')}
    for prefix, lang in [('', 'en'), ('pt-br/', 'pt-BR')]:
        for slug in ['', *project_ids]:
            page = out / prefix / (f'projects/{slug}' if slug else '') / 'index.html'
            doc = docs[page]
            expected = 0 if slug else 2
            if (doc.lang, doc.h1, doc.quotes, doc.japanese) != (lang, 1, expected, expected):
                raise ValueError(f'Invalid language, heading, quotations or signature in {page}')
    if len(docs) != 2 * (1 + len(project_ids)):
        raise ValueError('The localized page sets differ')
    for page, doc in docs.items():
        for ref in doc.refs:
            parts = urlsplit(ref)
            if parts.scheme in {'https','mailto'}:
                continue
            if parts.scheme or parts.netloc or parts.path.startswith('/'):
                raise ValueError(f'Unexpected URL in {page}: {ref}')
            dest = (page.parent / unquote(parts.path)).resolve() if parts.path else page
            if dest.is_dir():
                dest /= 'index.html'
            if not dest.is_relative_to(out) or not dest.is_file():
                raise ValueError(f'Missing local target in {page}: {ref}')
            if parts.fragment and (dest not in docs or unquote(parts.fragment) not in docs[dest].ids):
                raise ValueError(f'Broken anchor in {page}: {ref}')
    for css in out.rglob('*.css'):
        for ref in re.findall(r'url\(["\']?([^)"\']+)', css.read_text(encoding='utf-8')):
            if not (css.parent / ref).is_file():
                raise ValueError(f'Missing stylesheet asset: {ref}')
    print(f'Validated {len(docs)} localized pages, internal links, anchors and stylesheet assets.')
