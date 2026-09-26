import os
import shutil
import urllib.request
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "closet-organizer-hanger")
QUALITY = 92
THUMB = 160
HERO_MOBILE = 800
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Full-size CDN assets from Allessya funnel (document order)
URLS = {
    "hero-product.png": "https://cdn.myshopage.com/4a89fa62-ff04-48ca-7dd7-e3ef33c38600/w1000.jpg",
    "hero-rotate.png": "https://cdn.myshopage.com/3d074f4b-b4a6-4cbb-ddf5-4a425c491300/w1000.jpg",
    "hero-hooks.png": "https://cdn.myshopage.com/59c9a228-261b-44cb-f714-0d13c5308600/w1000.jpg",
    "hero-space.png": "https://cdn.myshopage.com/aed5ed65-5e4b-4c84-9134-c169cdd47600/w1000.jpg",
    "story-problem.png": "https://cdn.myshopage.com/1069a40d-dd99-4da3-c749-a5ae4ff4a800/w1000.jpg",
    "story-solution.png": "https://cdn.myshopage.com/57139ae4-6117-4100-e56d-3c378d1c5f00/w1000.jpg",
    "benefit-1.png": "https://cdn.myshopage.com/30673704-53d4-4a0f-de5c-7ec786c7a000/w1000.png",
    "benefit-2.png": "https://cdn.myshopage.com/bb27c8cd-e5ff-43f5-c69a-89284744a900/w1000.jpg",
    "benefit-3.png": "https://cdn.myshopage.com/8d0627d6-5092-414f-17e5-5317b7cbcd00/w1000.png",
    "benefit-4.png": "https://cdn.myshopage.com/240187f6-9c88-444d-f62f-cc4e86bece00/w1000.png",
    "benefit-5.png": "https://cdn.myshopage.com/431431de-f917-4483-c992-1266801d8800/w1000.jpg",
    "benefit-6.png": "https://cdn.myshopage.com/e745f1e6-aefc-4717-a024-200be61b0000/w1000.png",
    "benefit-7.png": "https://cdn.myshopage.com/f7c23ce4-f289-4ecc-2358-611fe12af100/w1000.png",
    "benefit-8.png": "https://cdn.myshopage.com/a2c611ba-87f3-4666-4ab4-c87c97c79d00/w1000.png",
    "how-to-demo.png": "https://cdn.myshopage.com/431431de-f917-4483-c992-1266801d8800/w1000.jpg",
}

os.makedirs(ROOT, exist_ok=True)

for name, url in URLS.items():
    dst = os.path.join(ROOT, name)
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        with open(dst, "wb") as f:
            f.write(data)
        print("ok", name, len(data))
    except Exception as e:
        print("fail", name, e)

for icon in ("icon-guarantee", "icon-shipping", "icon-cod"):
    src = os.path.join(os.path.dirname(__file__), "..", "images", "dumpling-maker-set", icon + ".png")
    dst = os.path.join(ROOT, icon + ".png")
    if os.path.exists(src):
        shutil.copy2(src, dst)

for name in sorted(f for f in os.listdir(ROOT) if f.lower().endswith(".png")):
    src = os.path.join(ROOT, name)
    if os.path.getsize(src) < 500:
        continue
    base = os.path.splitext(name)[0]
    dst = os.path.join(ROOT, base + ".webp")
    im = Image.open(src).convert("RGBA")
    if max(im.size) > 1500:
        ratio = 1500 / max(im.size)
        im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    if name.startswith("hero-") and "-thumb" not in name:
        ratio = THUMB / max(im.size)
        thumb = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
        thumb.save(os.path.join(ROOT, base + "-thumb.webp"), "WEBP", quality=90, method=6)
    if name == "hero-product.png":
        if im.width > HERO_MOBILE:
            ratio = HERO_MOBILE / im.width
            mobile = im.resize((HERO_MOBILE, max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
        else:
            mobile = im
        mobile.save(os.path.join(ROOT, "hero-product-800.webp"), "WEBP", quality=QUALITY, method=6)

print("done")
