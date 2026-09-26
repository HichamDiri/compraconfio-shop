import os
import shutil
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "closet-organizer-hanger")
ASSETS = r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
SRC = [
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_1__3_-0319dba3-54f7-402d-bc92-a59794221d14.png",
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_ChatGPT_Image_26_sept._2026__17_48_05-d3a0a02d-56df-46c0-a69d-c7afb25a98a4.png",
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_3__3_-960b7f3f-8b3c-42ad-a329-241d34316685.png",
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_4__3_-eac697b4-310a-4116-b581-0b24e0c36f40.png",
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_5__3_-5e3cc35e-bdc7-4cbc-a11d-98a5e7f8e93b.png",
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_6__3_-454749a9-adef-4167-9a54-9c13659fad1e.png",
    "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_7__2_-1dd51523-04fd-490a-8b8d-f3c74dd3b539.png",
]
MAX = 1500
QUALITY = 92

for i, name in enumerate(SRC, start=1):
    src = os.path.join(ASSETS, name)
    dst_png = os.path.join(ROOT, f"benefit-{i}.png")
    shutil.copy2(src, dst_png)
    im = Image.open(dst_png).convert("RGBA")
    if max(im.size) > MAX:
        r = MAX / max(im.size)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.Resampling.LANCZOS)
        im.save(dst_png, "PNG")
    im.save(os.path.join(ROOT, f"benefit-{i}.webp"), "WEBP", quality=QUALITY, method=6)
    print("ok", i)
