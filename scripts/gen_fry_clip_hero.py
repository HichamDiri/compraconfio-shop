import os
import shutil
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "frying-filter-clip")
ASSETS = r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
QUALITY = 92
THUMB = 160
HERO_MOBILE = 800
MAX_SIDE = 1500

MAP = [
    ("c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_ChatGPT_Image_25_sept._2026__12_30_43-b9268798-ee72-4479-9922-759391a15cd1.png", "hero-product"),
    ("c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_ChatGPT_Image_25_sept._2026__12_30_47-9a6a2177-766d-42a5-89ec-9acb1484290b.png", "hero-crisp"),
    ("c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_ChatGPT_Image_25_sept._2026__12_30_50-639025fe-750a-4afe-b8b4-dd6539aa2c3e.png", "hero-daily"),
    ("c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_ChatGPT_Image_25_sept._2026__12_31_02-7515b743-c6c8-4eb3-a86f-5aaf90b8815b.png", "hero-control"),
]

os.makedirs(ROOT, exist_ok=True)

for src_name, base in MAP:
    src = os.path.join(ASSETS, src_name)
    png = os.path.join(ROOT, base + ".png")
    shutil.copy2(src, png)
    im = Image.open(png).convert("RGBA")
    if max(im.size) > MAX_SIDE:
        ratio = MAX_SIDE / max(im.size)
        im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
        im.save(png, "PNG")
    webp = os.path.join(ROOT, base + ".webp")
    im.save(webp, "WEBP", quality=QUALITY, method=6)
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
    print(base, os.path.getsize(png) // 1024, "KB png,", os.path.getsize(webp) // 1024, "KB webp")
