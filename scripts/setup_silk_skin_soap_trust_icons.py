from pathlib import Path

from PIL import Image

ASSETS = Path(
    r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "silk-skin-soap"

ICONS: list[tuple[str, Path]] = [
    (
        "icon-guarantee",
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_Untitled_design__61_-a21835d8-d0c6-4af1-a2e2-4f2dcad4baf7.png",
    ),
    (
        "icon-shipping",
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_Untitled_design__59_-f8165257-86e7-4ea8-9b1f-7ad3c196d67e.png",
    ),
    (
        "icon-cod",
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_Untitled_design__60_-99fbde9b-7b9b-4df0-b41e-bb4840f9795f.png",
    ),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in ICONS:
        im = Image.open(src).convert("RGBA")
        w, h = im.size
        side = max(w, h)
        sq = Image.new("RGBA", (side, side), (255, 255, 255, 0))
        sq.paste(im, ((side - w) // 2, (side - h) // 2), im)
        out = sq.copy()
        out.thumbnail((96, 96), Image.Resampling.LANCZOS)
        out.save(OUT / f"{name}.png", "PNG", optimize=True)
        out.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6)
        print(name, out.size)
    print("done")


if __name__ == "__main__":
    main()
