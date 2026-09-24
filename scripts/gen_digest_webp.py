import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "digest-capsules")
QUALITY = 92
THUMB = 160
HERO_MOBILE = 800
REVIEW_MAX = 800

for name in sorted(f for f in os.listdir(ROOT) if f.lower().endswith(".png")):
    src = os.path.join(ROOT, name)
    base = os.path.splitext(name)[0]
    dst = os.path.join(ROOT, base + ".webp")
    im = Image.open(src).convert("RGBA")

    if name.startswith("review-"):
        w, h = im.size
        if max(w, h) > REVIEW_MAX:
            ratio = REVIEW_MAX / max(w, h)
            im = im.resize(
                (max(1, int(w * ratio)), max(1, int(h * ratio))),
                Image.Resampling.LANCZOS,
            )

    im.save(dst, "WEBP", quality=QUALITY, method=6)
    png_kb = os.path.getsize(src) // 1024
    webp_kb = os.path.getsize(dst) // 1024
    print(f"{name}: {png_kb}KB -> {webp_kb}KB")

    if name.startswith("hero-") and "-thumb" not in name:
        ratio = THUMB / max(im.size)
        thumb = im.resize(
            (max(1, int(im.width * ratio)), max(1, int(im.height * ratio))),
            Image.Resampling.LANCZOS,
        )
        thumb.save(os.path.join(ROOT, base + "-thumb.webp"), "WEBP", quality=90, method=6)

    if name == "hero-product.png":
        if im.width > HERO_MOBILE:
            ratio = HERO_MOBILE / im.width
            mobile = im.resize(
                (HERO_MOBILE, max(1, int(im.height * ratio))),
                Image.Resampling.LANCZOS,
            )
        else:
            mobile = im
        mobile.save(os.path.join(ROOT, "hero-product-800.webp"), "WEBP", quality=QUALITY, method=6)
