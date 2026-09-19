import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "rfid-card-holder")
QUALITY = 92
THUMB = 160

for name in sorted(f for f in os.listdir(ROOT) if f.lower().endswith(".png")):
    src = os.path.join(ROOT, name)
    base = os.path.splitext(name)[0]
    dst = os.path.join(ROOT, base + ".webp")
    im = Image.open(src).convert("RGBA")
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    if name.startswith("hero-") and "-thumb" not in name:
        ratio = THUMB / max(im.size)
        thumb = im.resize(
            (max(1, int(im.width * ratio)), max(1, int(im.height * ratio))),
            Image.Resampling.LANCZOS,
        )
        thumb.save(os.path.join(ROOT, base + "-thumb.webp"), "WEBP", quality=90, method=6)
    print(f"{name}: {os.path.getsize(src) // 1024}KB -> {os.path.getsize(dst) // 1024}KB")

gif_path = os.path.join(ROOT, "how-to-use.gif")
poster_path = os.path.join(ROOT, "how-to-use-poster.webp")
if os.path.exists(gif_path):
    gif = Image.open(gif_path)
    gif.seek(0)
    poster = gif.convert("RGBA")
    poster.save(poster_path, "WEBP", quality=90, method=6)
    print(f"poster: {os.path.getsize(poster_path) // 1024}KB")
