from pathlib import Path

from PIL import Image

ASSETS = Path(
    r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "silk-skin-soap"

# User images 1–6 → benefit slots on the page (4 and 6 cards removed)
SOURCES: list[tuple[int, Path]] = [
    (
        1,
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_1__2_-9058101b-1483-406a-8034-d7b5d4d41a87.png",
    ),
    (
        2,
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_2__2_-d4790049-ff20-4ea6-8026-598db90422b7.png",
    ),
    (
        3,
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_3__2_-9460ac0c-b16e-45e7-8536-206a7db07105.png",
    ),
    (
        5,
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_4-e88ed404-7c56-4745-9c42-e62de34ea4f0.png",
    ),
    (
        7,
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_5-f68e50d8-d6b4-49de-a93b-5c1faeeff6a3.png",
    ),
    (
        8,
        ASSETS
        / "c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_benefits_6-f0895b9d-4082-4b72-9ab7-c9e248bf4eed.png",
    ),
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
    for num, src in SOURCES:
        im = to_square(Image.open(src))
        thumb = im.copy()
        thumb.thumbnail((800, 800), Image.Resampling.LANCZOS)
        thumb.save(OUT / f"benefit-{num}.png", "PNG", optimize=True)
        thumb.save(OUT / f"benefit-{num}.webp", "WEBP", quality=84, method=6)
        print("benefit", num, src.name)
    print("done")


if __name__ == "__main__":
    main()
