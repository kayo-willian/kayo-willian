#!/usr/bin/env python3
"""Build the bilingual static portfolio using the Python standard library."""
import hashlib
from pathlib import Path
from shutil import copyfile, rmtree

from generator.common import ROOT, Page, data
from generator.home import home
from generator.projects import project_page
from generator.validation import verify


def copy_assets(out):
    assets = {}
    for folder in ['assets', 'src']:
        base = ROOT / folder
        for file in sorted(base.rglob('*')):
            if not file.is_file() or file.name == 'reflector.svg':
                continue
            path = file.relative_to(base)
            if file.suffix in {'.js', '.css'}:
                digest = hashlib.sha256(file.read_bytes()).hexdigest()[:12]
                dest = Path('assets') / f'{file.stem}.{digest}{file.suffix}'
            else:
                dest = Path('assets') / path
            assets[path.as_posix()] = dest.as_posix()
            (out / dest).parent.mkdir(parents=True, exist_ok=True)
            copyfile(file, out / dest)
    return assets


def write(out, page, html):
    dest = out / page.path / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding='utf-8')


def main():
    out = ROOT / 'dist'
    if out.exists():
        rmtree(out)
    assets = copy_assets(out)
    projects = data('projects')
    for lang in ['en', 'pt']:
        page = Page(lang, assets)
        write(out, page, home(page, projects))
        for index, item in enumerate(projects):
            page = Page(lang, assets, item['id'])
            next_item = projects[(index + 1) % len(projects)]
            write(out, page, project_page(page, item, next_item))
    (out / '.nojekyll').touch()
    verify(out, [p['id'] for p in projects])


if __name__ == '__main__':
    main()
