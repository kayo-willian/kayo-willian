"""Create portfolio crops and photographic montages from original repository assets.
Sources: Arduino images 01, 08 and 14; Scroll Lock images 1-original and
2-original; Channel Blue assets/banner.png. No generated hardware or game art.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT / 'media'
OUT = ROOT.parent / 'assets' / 'images'
SIZE = (1200, 480)
BG = (6, 12, 21)
LINE = (43, 73, 108)


def load(name, crop=None):
    with Image.open(MEDIA / name) as original:
        im = ImageOps.exif_transpose(original).convert('RGBA')
    if crop:
        w, h = im.size
        im = im.crop(tuple(round(v * (w if i % 2 == 0 else h)) for i, v in enumerate(crop)))
    return im


def canvas():
    im = Image.new('RGBA', SIZE, BG + (255,))
    d = ImageDraw.Draw(im)
    for x in range(SIZE[0]):
        a = x / (SIZE[0] - 1)
        d.line((x, 0, x, SIZE[1]), fill=(round(6+5*a), round(12+13*a), round(21+23*a), 255))
    return im


def panel(im, image, rect, fit=False):
    x, y, w, h = rect
    d = ImageDraw.Draw(im)
    d.rectangle((x-1, y-1, x+w, y+h), fill=LINE)
    d.rectangle((x, y, x+w-1, y+h-1), fill=BG)
    if fit:
        pic = ImageOps.fit(image, (w, h), method=Image.Resampling.LANCZOS)
    else:
        pic = ImageOps.contain(image, (w, h), method=Image.Resampling.LANCZOS)
    im.alpha_composite(pic, (x+(w-pic.width)//2, y+(h-pic.height)//2))


def save(im, name):
    im.convert('RGB').save(OUT / name, 'WEBP', quality=88, method=6)


def arduino():
    im = canvas()
    # Wide view retains board, wires, all three buttons and the potentiometer.
    panel(im, load('arduino-prototype.jpeg', (.18,.035,.97,.965)), (18,18,610,444))
    # Independent crops from the original photographs retain the actual components.
    panel(im, load('arduino-board.jpeg', (.18,.34,.50,.585)), (646,18,536,211))
    panel(im, load('arduino-controls.jpeg', (.10,.53,.66,.97)), (646,247,536,215))
    save(im, 'arduino-linux-controller.webp')


def scrolllock():
    im = canvas()
    panel(im, load('keyboard-full.png', (0,.18,1,1)), (18,18,760,444))
    panel(im, load('keyboard-detail.png', (.17,.17,.84,.96)), (796,18,386,444))
    save(im, 'scrolllock-rgb-fix.webp')


def channel():
    # The 2.5:1 crop removes only the top/bottom margins of the wide original;
    # the central mascot and original title remain intact.
    im = ImageOps.fit(load('channel-blue-banner.png'), SIZE,
                      method=Image.Resampling.LANCZOS, centering=(.5,.5))
    save(im, 'channel-blue.webp')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    arduino()
    scrolllock()
    channel()
