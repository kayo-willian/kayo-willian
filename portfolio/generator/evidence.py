"""Prepare a publication-safe, optimized copy of the documented NOC rack photograph."""
from pathlib import Path
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def prepare(source, target):
    with Image.open(source) as original:
        im = ImageOps.exif_transpose(original)
        w,h = im.size
        im = im.crop((int(w*.04),int(h*.24),int(w*.98),int(h*.95)))
        im = ImageOps.fit(im,(1240,760),method=Image.Resampling.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(1.10)
        im = ImageEnhance.Brightness(im).enhance(.94)
        # Conceal the institutional and inventory stickers without altering equipment.
        for box in [(850,141,1058,203),(280,383,479,446)]:
            im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(23)),box)
        im.save(target,quality=86)

if __name__ == '__main__':
    prepare(Path(sys.argv[1]),Path(sys.argv[2]))
