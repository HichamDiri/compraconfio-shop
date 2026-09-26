import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "closet-organizer-hanger")
HERO = ("hero-product", "hero-rotate", "hero-hooks", "hero-space")
QUALITY = 92
THUMB = 160
HERO_MOBILE = 800

for base in HERO:
    src = os.path.join(ROOT, base + ".png")
    im = Image.open(src).convert("RGBA")
    if max(im.size) > 1500:
        ratio = 1500 / max(im.size)
        im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
    im.save(os.path.join(ROOT, base + ".webp"), "WEBP", quality=QUALITY, method=6)
    ratio = THUMB / max(im.size)
    thumb = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
    thumb.save(os.path.join(ROOT, base + "-thumb.webp"), "WEBP", quality=90, method=6)
    if base == "hero-product":
        if im.width > HERO_MOBILE:
            ratio = HERO_MOBILE / im.width
            mobile = im.resize((HERO_MOBILE, max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
        else:
            mobile = im
        mobile.save(os.path.join(ROOT, "hero-product-800.webp"), "WEBP", quality=QUALITY, method=6)
print("ok")
