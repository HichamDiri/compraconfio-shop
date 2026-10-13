"""Generate metabolae-ceylon-cinnamon.css from nattokinase-hale.css."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
css = (root / "css" / "nattokinase-hale.css").read_text(encoding="utf-8")
css = css.replace(
    'body[data-product="natto-pa"], body[data-product="digest-pa"]',
    'body[data-product="cinnamon-pa"]',
)
css = css.replace('body[data-product="natto-pa"]', 'body[data-product="cinnamon-pa"]')
css = css.replace('body[data-product="digest-pa"]', 'body[data-product="cinnamon-pa"]')
css = css.replace(
    "/* Nattokinasa Panamá — Hale Heart layout */",
    "/* Metabolae Ceylon Cinnamon Panamá — Hale-style layout */",
)
css = css.replace("--hl-crimson: #4B2904;", "--hl-crimson: #7B4A2E;")
css = css.replace("--hl-crimson-bright: #624010;", "--hl-crimson-bright: #9A6238;")
css = css.replace("--hl-crimson-deep: #351C03;", "--hl-crimson-deep: #5C3318;")
css = css.replace("--hl-copper: #b87333;", "--hl-copper: #C4844A;")
out = root / "css" / "metabolae-ceylon-cinnamon.css"
out.write_text(css, encoding="utf-8")
print("Wrote", out)
