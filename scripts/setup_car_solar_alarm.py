"""Setup car solar alarm LED Panama page assets."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
assets = Path(r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets")
dest_dir = root / "images" / "car-solar-alarm-led"
dest_dir.mkdir(parents=True, exist_ok=True)

matches = list(assets.glob("*imgi_1_41Zi66WNXgL*"))
if matches:
    data = Path("\\\\?\\" + str(matches[0])).read_bytes()
    (dest_dir / "hero-product.jpg").write_bytes(data)
    print("hero-product.jpg", len(data))
else:
    print("WARN: hero asset not found")

css = (root / "css" / "steel-fryer.css").read_text(encoding="utf-8")
css = css.replace('body[data-product="steel-fryer"]', 'body[data-product="car-alarm-led"]')
css = css.replace("--fryer-", "--alarm-")
css = css.replace(".dot.fryer", ".dot.alarm")
css = css.replace("--alarm-purple:", "--alarm-red:")
css = css.replace("--alarm-purple-deep:", "--alarm-red-deep:")
header = "/* Luz LED alarma solar para auto — CompraConfio Panamá */\n"
if not css.startswith("/* Luz LED"):
    css = header + css
(root / "css" / "car-solar-alarm-led.css").write_text(css, encoding="utf-8")
print("car-solar-alarm-led.css ok")
