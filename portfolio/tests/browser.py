"""Exercise the Pages build at its repository prefix, in a real Chromium browser."""
import argparse
from pathlib import Path
from urllib.parse import unquote, urlparse

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / 'dist'
BASE = 'https://portfolio.test/kayo-willian/'
VIEWPORTS = [(1920,1080), (1440,900), (1366,768), (768,1024), (390,844)]


def serve(route):
    url = route.request.url
    if not url.startswith(BASE):
        raise AssertionError(f'Unexpected request: {url}')
    path = (OUT / unquote(urlparse(url[len(BASE):]).path)).resolve()
    if path.is_dir():
        path /= 'index.html'
    assert path.is_relative_to(OUT) and path.is_file(), url
    route.fulfill(path=path)


def check_width(page, width):
    assert page.locator('html').evaluate('(el) => el.scrollWidth <= innerWidth'), (page.url, width)


def capture(page, folder, name):
    if folder:
        page.screenshot(path=folder / f'{name}.png', full_page=True, animations='disabled')


def check_home(page, base, width, lang, folder):
    page.goto(base + ('pt-br/' if lang == 'pt' else ''))
    page.evaluate('document.fonts.ready')
    assert page.locator('html').get_attribute('lang') == ('pt-BR' if lang == 'pt' else 'en')
    check_width(page, width)
    assert page.locator('[lang="ja"]').count() == 2
    assert page.evaluate("document.fonts.check('700 30px Kana', 'ゴー・ビヨンド')")
    assert page.locator('blockquote').count() == 2
    for image in page.locator('img').all():
        image.scroll_into_view_if_needed()
        image.evaluate('(img) => img.decode()')
    page.evaluate('scrollTo(0,0)')
    capture(page, folder, f'{lang}-{width}')
    if width == 390:
        menu = page.locator('.menu')
        menu.click()
        assert page.locator('#nav').is_visible()
        if folder:
            page.screenshot(path=folder / f'{lang}-menu.png')
        page.keyboard.press('Escape')
        assert menu.get_attribute('aria-expanded') == 'false'
        menu.click()
        page.locator('#nav a[href="#labs"]').click()
        assert menu.get_attribute('aria-expanded') == 'false'
    else:
        page.locator('#nav a[href="#labs"]').click()
    lab = page.locator('#linux-networking-labs')
    assert lab.locator('.lab-body').is_visible()
    assert page.locator('.lab-body:visible').count() == 4
    assert page.locator('.project-card').count() == 6
    assert page.locator('.hero-brand .kana').is_visible()
    assert page.locator('.antenna').count() == 0
    page.locator('.language').click()
    assert page.url.endswith('#labs')
    page.locator('.lead-copy a').first.click()
    assert 'projects/enterprise-noc-from-scratch/' in page.url
    check_width(page, width)
    page.locator('.language').click()
    assert page.locator('html').get_attribute('lang') == ('pt-BR' if lang == 'pt' else 'en')
    capture(page, folder, f'{lang}-case-{width}')
    page.locator('.breadcrumb').click()
    assert page.url.endswith('#work')
    if width == 390:
        for case in sorted(OUT.glob('projects/*/index.html')):
            url = base + ('pt-br/' if lang == 'pt' else '') + f'projects/{case.parent.name}/'
            page.goto(url)
            page.evaluate('document.fonts.ready')
            check_width(page, width)
            assert page.locator('h1').inner_text()
            assert page.locator('.case-sources a').count() >= 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chromium')
    parser.add_argument('--screenshots', type=Path)
    parser.add_argument('--live', help='Test a deployed Pages URL instead of the local artifact')
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=args.chromium)
        for width, height in VIEWPORTS:
            ctx = browser.new_context(viewport={'width':width,'height':height}, reduced_motion='reduce')
            if not args.live:
                ctx.route('**/*', serve)
            page = ctx.new_page()
            page.on('pageerror', lambda err: errors.append(str(err)))
            page.on('response', lambda res: errors.append(f'{res.status} {res.url}') if res.status >= 400 else None)
            for lang in ['en','pt']:
                check_home(page, args.live or BASE, width, lang, args.screenshots)
            ctx.close()
        ctx = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
        if not args.live:
            ctx.route('**/*', serve)
        page = ctx.new_page()
        page.goto(args.live or BASE)
        assert page.locator('#nav').is_visible()
        page.locator('#nav a[href="#labs"]').click()
        assert page.locator('#linux-networking-labs .lab-body').is_visible()
        ctx.close()
        browser.close()
    assert not errors, errors
    print('Chromium passed both languages at all five widths, including navigation and case studies.')


if __name__ == '__main__':
    main()
