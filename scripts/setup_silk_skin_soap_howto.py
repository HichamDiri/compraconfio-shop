import shutil
from pathlib import Path

from PIL import Image

SRC_GIF = Path(r"D:\download\SOAP\1008.gif")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "silk-skin-soap"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dst_gif = OUT / "how-to-demo.gif"
    shutil.copy2(SRC_GIF, dst_gif)

    im = Image.open(dst_gif)
    im.seek(0)
    frame = im.convert("RGB")
    w, h = frame.size
    side = max(w, h)
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(frame, ((side - w) // 2, (side - h) // 2))
    poster = sq.copy()
    poster.thumbnail((800, 800), Image.Resampling.LANCZOS)
    poster.save(OUT / "how-to-demo-poster.webp", "WEBP", quality=88, method=6)
    print("gif", dst_gif.stat().st_size // 1024, "KB")
    print("poster", (OUT / "how-to-demo-poster.webp").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
