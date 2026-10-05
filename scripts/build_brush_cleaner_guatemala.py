import os
import re
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")
src_html = subprocess.check_output(
    ["git", "show", "HEAD:makeup-brush-cleaner-panama.html"],
    cwd=ROOT,
    text=True,
    encoding="utf-8",
)

css_src = subprocess.check_output(
    ["git", "show", "HEAD:css/makeup-brush-cleaner.css"],
    cwd=ROOT,
    text=True,
    encoding="utf-8",
)

out_path = os.path.join(ROOT, "makeup-brush-cleaner-panama.html")
css_path = os.path.join(ROOT, "css", "makeup-brush-cleaner.css")

html = src_html

replacements = [
    ("Panamá", "Guatemala"),
    ("panama", "guatemala"),
    ("Panama", "Guatemala"),
    ('data-country="PA"', 'data-country="GT"'),
    ('data-thankyou="/thank-you-compraconfio-panama.html"', 'data-thankyou="/thank-you-compraconfio.html"'),
    ('action="/thank-you-compraconfio-panama.html"', 'action="/thank-you-compraconfio.html"'),
    ('data-abandon-checkout="on"', 'data-abandon-checkout="off"'),
    ("/js/pa-locations.js", "/js/gt-locations.js"),
    ('name="country" id="country" value="Panamá"', 'name="country" id="country" value="Guatemala"'),
    ('name="currency" value="USD"', 'name="currency" value="GTQ"'),
    ("makeup-brush-cleaner-panama", "makeup-brush-cleaner-guatemala"),
    ("cc-brush-cleaner-pa-", "cc-brush-cleaner-gt-"),
    ("Selecciona tu provincia", "Selecciona tu departamento"),
    ("Selecciona tu distrito", "Selecciona tu municipio"),
    ("WhatsApp (ej. 6123 4567)", "WhatsApp (ej. 5123 4567)"),
    ("Enviamos a todas las provincias de Panamá", "Enviamos a todos los departamentos de Guatemala"),
    ("Envío gratis a toda Panamá", "Envío gratis a toda Guatemala"),
    ("pa-locations", "gt-locations"),
    ("PA_DISTRITOS", "GT_MUNICIPIOS"),
    ("distritos", "municipios"),
]

for old, new in replacements:
    html = html.replace(old, new)

html = re.sub(
    r"<title>[^<]+</title>",
    "<title>Limpiadora Eléctrica de Brochas | CompraConfio Guatemala — Pago Contra Entrega</title>",
    html,
    count=1,
)
html = re.sub(
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Limpiadora eléctrica de brochas de maquillaje. Rotación automática y USB. Envío gratis y pago contra entrega en Guatemala. Precio Q229.">',
    html,
    count=1,
)

# Single bundle Q229
bundle_block = """        <div class="bundles">
          <label class="bundle bundle-option is-selected">
            <input type="radio" name="bundleOption" value="cc-brush-cleaner-gt-1" data-product-id="cc-brush-cleaner-gt-1" data-product-name="Limpiadora Eléctrica de Brochas - 1 unidad" data-price="229" data-old-price="320" data-save="28" data-label="1 Unidad" checked>
            <div class="bundle-card">
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>1 Unidad</span>
                <span class="bundle-cost"><strong>Q229</strong><del>Q320</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot brush"></span>Limpiadora eléctrica + cable USB</span>
              </div>
            </div>
          </label>
        </div>"""

html = re.sub(r"<div class=\"bundles\">.*?</div>\s*<div class=\"form-head\">", bundle_block + "\n        <div class=\"form-head\">", html, count=1, flags=re.DOTALL)

# Hero pricing
html = re.sub(
    r'<span class="price-now" id="priceNow">\$[^<]+</span>\s*<span class="price-was" id="priceWas">\$[^<]+</span>\s*<span class="price-save">[^<]+</span>',
    '<span class="price-now" id="priceNow">Q229</span>\n        <span class="price-was" id="priceWas">Q320</span>\n        <span class="price-save" id="priceSave">Ahorra 28%</span>',
    html,
    count=1,
)

html = html.replace('<strong id="stickyPrice">$30</strong>', '<strong id="stickyPrice">Q229</strong>')
html = html.replace('id="orderTotal" value="30"', 'id="orderTotal" value="229"')
html = re.sub(
    r'<strong id="sumSubtotal">\$[^<]+</strong>',
    '<strong id="sumSubtotal">Q229</strong>',
    html,
    count=1,
)
html = re.sub(
    r'<strong id="sumTotal">\$[^<]+</strong>',
    '<strong id="sumTotal">Q229</strong>',
    html,
    count=1,
)
html = html.replace('data-cost="5"', 'data-cost="25"')
html = html.replace('<span class="ship-cost">$5</span>', '<span class="ship-cost">Q25</span>')

# syncOrder for GTQ
sync_old = """    priceNow.textContent = '$' + subtotal;
    priceWas.textContent = '$' + bundle.dataset.oldPrice;
    stickyPrice.textContent = '$' + subtotal;"""
sync_new = """    priceNow.textContent = 'Q' + subtotal;
    priceWas.textContent = 'Q' + bundle.dataset.oldPrice;
    var priceSave = document.getElementById('priceSave');
    if (priceSave && bundle.dataset.save) priceSave.textContent = 'Ahorra ' + bundle.dataset.save + '%';
    stickyPrice.textContent = 'Q' + subtotal;"""
html = html.replace(sync_old, sync_new)
html = html.replace("sumSubtotal.textContent = '$' + subtotal;", "sumSubtotal.textContent = 'Q' + subtotal;")
html = html.replace("sumShipping.textContent = ship ? '$' + ship : 'Gratis';", "sumShipping.textContent = ship ? 'Q' + ship : 'Gratis';")
html = html.replace("sumTotal.textContent = '$' + total;", "sumTotal.textContent = 'Q' + total;")

html = html.replace("© 2026 CompraConfio — Guatemala", "© 2026 CompraConfio — Guatemala")

with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

with open(css_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(css_src)

print("wrote", out_path)
