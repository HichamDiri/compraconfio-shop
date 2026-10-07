from pathlib import Path

from PIL import Image

ASSETS = Path(
    r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "thermal-wristband"

SOURCES = [
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_1__2_-39198819-cc28-41ad-bdf3-e3702799580f.png",
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_2__2_-c9254749-0968-4dcc-8ad7-a1928d67f959.png",
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_3__2_-b51dd908-76e9-4ec4-818b-db556c2b3827.png",
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_4-8c8e41f4-4907-45cf-81e5-ba188ddf7abc.png",
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_5-0de979a2-5730-4bc8-b26f-8548ae18d4a2.png",
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_6-9f71bc73-fd62-4891-8ad3-dbf4fcdc0895.png",
    ASSETS
    / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_7-3c8ad432-2af2-493d-8f72-c94e163e628e.png",
]


def to_square(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    side = max(w, h)
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(im, ((side - w) // 2, (side - h) // 2))
    return sq


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for i, src in enumerate(SOURCES, start=1):
        im = to_square(Image.open(src))
        thumb = im.copy()
        thumb.thumbnail((800, 800), Image.Resampling.LANCZOS)
        thumb.save(OUT / f"benefit-{i}.png", "PNG", optimize=True)
        thumb.save(OUT / f"benefit-{i}.webp", "WEBP", quality=84, method=6)
        print("benefit", i, src.name)
    print("done")


if __name__ == "__main__":
    main()
