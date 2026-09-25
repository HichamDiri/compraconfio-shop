import json
import os
import re
import shutil
import urllib.request
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "dumpling-maker-set")
SRC_HERO = r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets\c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_61O3fgnyUkL._AC_SL1001_-fc48d090-3a85-4716-9d20-2f5388307780.png"
PRODUCT_URL = "https://thegiftnorth.com/products/products-stainless-steel-dumpling-maker-set"
QUALITY = 92
THUMB = 160
HERO_MOBILE = 800

MAP = {
    0: "hero-product.png",
    1: "hero-uniform.png",
    2: "hero-fast.png",
    3: "hero-family.png",
    4: "story-problem.png",
    5: "story-solution.png",
    6: "benefit-1.png",
    7: "benefit-2.png",
    8: "benefit-3.png",
    9: "benefit-4.png",
    10: "benefit-5.png",
    11: "benefit-6.png",
    12: "benefit-7.png",
    13: "how-to-demo.png",
}

os.makedirs(ROOT, exist_ok=True)

js_url = PRODUCT_URL.split("?")[0] + ".js"
product = json.loads(urllib.request.urlopen(js_url, timeout=60).read().decode("utf-8", "ignore"))
urls = []
for img in product.get("images", []):
    u = re.sub(r"\?.*", "", str(img))
    if u.startswith("//"):
        u = "https:" + u
    if u and u not in urls:
        urls.append(u + "?width=1500")

print("found", len(urls), "shopify images")

for i, name in MAP.items():
    dst = os.path.join(ROOT, name)
    if name == "hero-product.png" and os.path.exists(SRC_HERO):
        shutil.copy2(SRC_HERO, dst)
        print("copied user hero")
        continue
    if i < len(urls):
        urllib.request.urlretrieve(urls[i], dst)
        print("downloaded", name)
    elif not os.path.exists(dst):
        print("missing", name)

for icon in ("icon-guarantee", "icon-shipping", "icon-cod"):
    src = os.path.join(os.path.dirname(__file__), "..", "images", "steel-fryer", icon + ".png")
    dst = os.path.join(ROOT, icon + ".png")
    if os.path.exists(src):
        shutil.copy2(src, dst)

for name in sorted(f for f in os.listdir(ROOT) if f.lower().endswith(".png")):
    src = os.path.join(ROOT, name)
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
    print(f"{name}: {os.path.getsize(src)//1024}KB -> {os.path.getsize(dst)//1024}KB")
