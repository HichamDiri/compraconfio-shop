import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "led-flashlight-stick")
QUALITY = 92
THUMB = 160
HERO_MOBILE = 800

for name in sorted(f for f in os.listdir(ROOT) if f.lower().endswith(".png")):
    src = os.path.join(ROOT, name)
    base = os.path.splitext(name)[0]
    dst = os.path.join(ROOT, base + ".webp")
    im = Image.open(src).convert("RGBA")
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    png_kb = os.path.getsize(src) // 1024
    webp_kb = os.path.getsize(dst) // 1024
    print(f"{name}: {png_kb}KB -> {webp_kb}KB")

    if name.startswith("hero-"):
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
        mobile_thumb = mobile.resize(
            (THUMB, max(1, int(mobile.height * THUMB / mobile.width))),
            Image.Resampling.LANCZOS,
        )
        mobile_thumb.save(os.path.join(ROOT, "hero-product-thumb.webp"), "WEBP", quality=90, method=6)

gif_path = os.path.join(ROOT, "story-solution.gif")
poster_path = os.path.join(ROOT, "story-solution-poster.webp")
anim_path = os.path.join(ROOT, "story-solution.webp")
if os.path.exists(gif_path):
    gif = Image.open(gif_path)
    gif.seek(0)
    poster = gif.convert("RGBA")
    poster.save(poster_path, "WEBP", quality=90, method=6)
    print(f"poster: {os.path.getsize(poster_path) // 1024}KB")

    frames, durations = [], []
    try:
        while True:
            frames.append(gif.copy().convert("RGBA"))
            durations.append(gif.info.get("duration", 40))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    if frames:
        frames[0].save(
            anim_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            quality=QUALITY,
            method=6,
        )
        print(f"anim webp: {len(frames)} frames, {os.path.getsize(anim_path) // 1024}KB")
