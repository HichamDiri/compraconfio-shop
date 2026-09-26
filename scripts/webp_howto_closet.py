from PIL import Image

p = r"C:\Users\Administrateur\Projects\compraconfio-shop\images\closet-organizer-hanger\how-to-demo.png"
im = Image.open(p).convert("RGBA")
if max(im.size) > 1500:
    r = 1500 / max(im.size)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.Resampling.LANCZOS)
    im.save(p, "PNG")
im.save(p.replace(".png", ".webp"), "WEBP", quality=92, method=6)
print("webp", im.size)
