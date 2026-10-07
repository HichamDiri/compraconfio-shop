"""One-off: images + CSS for thermal-wristband Panama page."""
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "images" / "thermal-wristband"
SRC = Path(
    r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
    r"\c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images"
    r"_imgi_1_71-b21kCjbL._AC_SL1254_-7562c299-71aa-4826-a75c-3b408cb01032.png"
)


def fit(im, max_side: int):
    out = im.copy()
    out.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return out


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    src = Image.open(SRC).convert("RGB")
    w, h = src.size
    side = max(w, h)
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(src, ((side - w) // 2, (side - h) // 2))
    hero = sq

    fit(hero, 1024).save(IMG / "hero-product.png", "PNG", optimize=True)
    fit(hero, 1024).save(IMG / "hero-product.webp", "WEBP", quality=82, method=6)
    fit(hero, 800).save(IMG / "hero-product-800.webp", "WEBP", quality=82, method=6)
    fit(hero, 160).save(IMG / "hero-product-thumb.webp", "WEBP", quality=80, method=6)

    for n in ("story-problem", "story-solution", "story-solution-poster", "how-to-demo"):
        fit(hero, 800).save(IMG / f"{n}.png", "PNG", optimize=True)
        fit(hero, 800).save(IMG / f"{n}.webp", "WEBP", quality=82, method=6)

    for i in range(1, 8):
        fit(hero, 800).save(IMG / f"benefit-{i}.png", "PNG", optimize=True)
        fit(hero, 800).save(IMG / f"benefit-{i}.webp", "WEBP", quality=82, method=6)

    dum = ROOT / "images" / "dumpling-maker-set"
    for icon in ("icon-guarantee", "icon-shipping", "icon-cod"):
        for ext in ("png", "webp"):
            p = dum / f"{icon}.{ext}"
            if p.exists():
                shutil.copy2(p, IMG / f"{icon}.{ext}")

    css_src = ROOT / "css" / "dumpling-maker-set.css"
    css_dst = ROOT / "css" / "thermal-wristband.css"
    text = css_src.read_text(encoding="utf-8")
    text = text.replace("Maker & Dough Cutter Set", "Thermal Wristband Panamá")
    text = text.replace("dumpling-maker", "thermal-wristband")
    text = text.replace("--dumpling-", "--wrist-")
    text = text.replace(".dot.dumpling", ".dot.wrist")
    for a, b in {
        "#dcfce7": "#ffedd5",
        "#15803d": "#ea580c",
        "#166534": "#c2410c",
        "#f8faf8": "#fffaf5",
        "#f0fdf4": "#fff7ed",
        "#d1e7dd": "#fed7aa",
        "#86a892": "#fdba74",
        "#ecfdf3": "#ffedd5",
    }.items():
        text = text.replace(a, b)
    css_dst.write_text(text, encoding="utf-8")
    print("wrote", IMG, css_dst)


if __name__ == "__main__":
    main()
