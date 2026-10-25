"""Build yesnap-creatine-women-panama funnel from metabolae template."""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "images" / "yesnap-creatine-women"
SRC_HTML = ROOT / "metabolae-ceylon-cinnamon-panama.html"
OUT_HTML = ROOT / "yesnap-creatine-women-panama.html"
CSS_OUT = ROOT / "css" / "yesnap-creatine-women.css"
CSS_SRC = ROOT / "css" / "metabolae-ceylon-cinnamon.css"
V = "20261025a"
IMG = "/images/yesnap-creatine-women"
USER_HERO = Path(
    r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets"
    r"\c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_d3649f2b2e19aa1c8aae661925f11963_images_imgi_186_d13aefdf96d2e1f552ea9c1738e3d425-8e3db6ea-5430-4669-8711-94a298c5e349.jpg"
)


def fetch_images() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    if USER_HERO.is_file():
        shutil.copy2(USER_HERO, IMG_DIR / "hero-product.jpg")

    url = "https://www.yesnap.com/products/yesnap-creatine.js"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.loads(urllib.request.urlopen(req, timeout=90).read().decode("utf-8"))
    images = data.get("images") or []
    names = [
        "hero-formula.jpg",
        "hero-benefits.jpg",
        "hero-how-to.jpg",
        "slide-4.jpg",
        "slide-5.jpg",
    ]
    for i, src in enumerate(images[:5]):
        if isinstance(src, dict):
            src = src.get("src", "")
        src = str(src).split("?")[0]
        if src.startswith("//"):
            src = "https:" + src
        if not src:
            continue
        out = IMG_DIR / (names[i] if i < len(names) else f"slide-{i + 1}.jpg")
        try:
            urllib.request.urlretrieve(src, out)
            print("saved", out.name)
        except OSError as err:
            print("skip", out.name, err)


def build_css() -> None:
    css = CSS_SRC.read_text(encoding="utf-8")
    css = css.replace('body[data-product="cinnamon-pa"]', 'body[data-product="creatine-pa"]')
    css = css.replace(
        "/* Metabolae Ceylon Cinnamon Panamá — Hale-style layout */",
        "/* YESNAP Creatine for Women Panamá — Hale-style layout */",
    )
    css = css.replace("--hl-crimson: #7B4A2E;", "--hl-crimson: #D63384;")
    css = css.replace("--hl-crimson-bright: #9A6238;", "--hl-crimson-bright: #E85A9A;")
    css = css.replace("--hl-crimson-deep: #5C3318;", "--hl-crimson-deep: #A61E4D;")
    css = css.replace("--hl-copper: #C4844A;", "--hl-copper: #F4A6C6;")
    css = css.replace("--hl-cream: #fbf7f2;", "--hl-cream: #fff5f9;")
    css = css.replace("--hl-cream-warm: #f7f1e6;", "--hl-cream-warm: #fceef4;")
    css = css.replace("--hl-beige: #efe5d2;", "--hl-beige: #fde8f0;")
    css = css.replace("--hl-pink: #efe4d6;", "--hl-pink: #fdd9e8;")
    css = css.replace("background: #f4efe6;", "background: #fff0f6;")
    CSS_OUT.write_text(css, encoding="utf-8")


def gallery_block() -> str:
    q = f"?v={V}"
    slides = [
        ("hero-product.jpg", "YESNAP Creatine for Women Peach Pout — bolsa con 30 sobres"),
        ("hero-formula.jpg", "Fórmula con creatina, colágeno y aminoácidos — sabor durazno"),
        ("hero-benefits.jpg", "Beneficios para rutina fitness y bienestar"),
        ("hero-how-to.jpg", "Sobres individuales — mezclar con agua"),
    ]
    parts = ['    <section class="gallery" id="heroSection">', '      <div class="gallery-stage" id="galleryTrack">']
    for file_name, alt in slides:
        parts.append("        <div class=\"slide\">")
        parts.append(
            f'          <img class="is-contain" src="{IMG}/{file_name}{q}" alt="{alt}" '
            'width="1024" height="1024" loading="lazy" decoding="async">'
        )
        parts.append("        </div>")
    parts[4] = parts[4].replace('loading="lazy"', 'loading="eager" fetchpriority="high"')
    parts.append("      </div>")
    parts.append('      <div class="gallery-dots" id="galleryDots" aria-hidden="true"></div>')
    parts.append('      <div class="gallery-thumbs">')
    for i, (file_name, alt) in enumerate(slides):
        active = " is-active" if i == 0 else ""
        lazy = "" if i == 0 else ' loading="lazy"'
        parts.append(
            f'        <button type="button" class="thumb{active}" aria-label="Foto {i + 1}">'
            f'<img src="{IMG}/{file_name}{q}" alt="" width="160" height="160" decoding="async"{lazy}></button>'
        )
    parts.append("      </div>")
    parts.append("    </section>")
    return "\n".join(parts)


def replace_gallery(html: str) -> str:
    return re.sub(
        r'<section class="gallery" id="heroSection">.*?</section>',
        gallery_block(),
        html,
        count=1,
        flags=re.S,
    )


def replace_voices(html: str) -> str:
    block = f"""<section class="voices" id="resenas">
  <div class="shell">
    <p class="hl-eyebrow">Experiencias reales</p>
    <h2 class="hl-title">Descubre las experiencias de otras clientas</h2>
    <p class="hl-lead">Opiniones sobre el sabor, la preparación y la experiencia de compra. Los resultados varían según cada persona.</p>

    <div class="voices-track">
      <article class="voice">
        <img src="{IMG}/hero-product.jpg?v={V}" alt="Cliente con YESNAP Creatine" width="640" height="640" loading="lazy" decoding="async">
        <p class="voice-name">Valeria R. · Panamá</p>
        <p><strong>Me gusta el sabor durazno.</strong> Lo tomo después del gym y se siente fácil de mantener. El sobre se mezcla bien con agua fría y no me deja grumos raros.</p>
        <cite>Reseña de cliente</cite>
      </article>
      <article class="voice">
        <img src="{IMG}/hero-formula.jpg?v={V}" alt="Cliente con creatina YESNAP" width="640" height="640" loading="lazy" decoding="async">
        <p class="voice-name">Daniela M. · San Miguelito</p>
        <p><strong>Práctica para mi rutina.</strong> Llevo los sobres en la bolsa del gym. Me ayuda a ser constante con mi entrenamiento de pierna y glúteos.</p>
        <cite>Reseña de cliente</cite>
      </article>
      <article class="voice">
        <img src="{IMG}/hero-benefits.jpg?v={V}" alt="Cliente satisfecha con YESNAP" width="640" height="640" loading="lazy" decoding="async">
        <p class="voice-name">Camila S. · David</p>
        <p><strong>Compra sencilla y entrega clara.</strong> Pedí con pago contra entrega y me confirmaron por WhatsApp. El producto llegó bien empacado.</p>
        <cite>Reseña de cliente</cite>
      </article>
    </div>
  </div>
</section>"""
    return re.sub(r'<section class="voices" id="resenas">.*?</section>', block, html, count=1, flags=re.S)


def replace_timeline(html: str) -> str:
    block = """<section class="hl-section hl-beige">
  <div class="shell">
    <p class="hl-eyebrow">Tu camino</p>
    <h2 class="hl-title">Tu camino hacia unos glúteos más sexys</h2>
    <p class="hl-lead">Los resultados varían de una persona a otra. La creatina no garantiza glúteos más grandes por sí sola; el desarrollo muscular depende del entrenamiento y otros factores.</p>
    <div class="tl" id="creatine-timeline">
      <div class="tl-step tl-step--left">
        <div class="tl-card">
          <h3>Días 1–7: Empieza tu rutina</h3>
          <ul>
            <li>Incorpora la creatina siguiendo las instrucciones de la etiqueta.</li>
            <li>Apoya tu rendimiento durante entrenamientos intensos.</li>
            <li>Empieza a trabajar por unos glúteos más fuertes.</li>
            <li>Construye hábitos que te acerquen a tus objetivos.</li>
          </ul>
        </div>
        <span class="tl-marker" aria-hidden="true"><svg class="tl-check" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10 17.5L19 7.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
      </div>
      <div class="tl-step tl-step--right">
        <div class="tl-card">
          <h3>Días 7–14: Mantén el enfoque</h3>
          <ul>
            <li>Sigue una rutina enfocada en desarrollar los glúteos.</li>
            <li>Trabaja en tu fuerza y rendimiento físico.</li>
            <li>Combina ejercicio, alimentación equilibrada y descanso.</li>
            <li>Mantén la constancia en tu camino hacia la figura que deseas.</li>
          </ul>
        </div>
        <span class="tl-marker" aria-hidden="true"><svg class="tl-check" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10 17.5L19 7.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
      </div>
      <div class="tl-step tl-step--left">
        <div class="tl-card">
          <h3>Semanas 3–4: Sigue construyendo tu progreso</h3>
          <ul>
            <li>Continúa trabajando por unos glúteos más fuertes y definidos.</li>
            <li>Mantén una rutina de entrenamiento adecuada.</li>
            <li>Dale a tu cuerpo tiempo para adaptarse.</li>
            <li>Celebra cada avance en tu camino hacia tus objetivos.</li>
          </ul>
        </div>
        <span class="tl-marker" aria-hidden="true"><svg class="tl-check" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10 17.5L19 7.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
      </div>
    </div>
    <p class="tl-footnote">*Suplemento alimenticio. No sustituye entrenamiento ni consejo médico. Sigue la porción indicada en la etiqueta.</p>
  </div>
</section>"""
    return re.sub(
        r'<section class="hl-section hl-beige">\s*<div class="shell">\s*<p class="hl-eyebrow">Qué esperar</p>.*?</section>',
        block,
        html,
        count=1,
        flags=re.S,
    )


def replace_faq(html: str) -> str:
    faqs = [
        ("¿Esta creatina es para mujeres?", "La creatina se utiliza tanto por mujeres como por hombres. Revisa la etiqueta para conocer la fórmula y comprobar si se adapta a tus necesidades."),
        ("¿Me ayudará a tener glúteos más grandes?", "La creatina puede apoyar el desarrollo muscular cuando se combina con entrenamiento de resistencia. No garantiza glúteos más grandes por sí sola."),
        ("¿Puedo conseguir resultados sin hacer ejercicio?", "No debes esperar que la creatina desarrolle tus glúteos sin entrenamiento. Su principal beneficio se relaciona con el rendimiento durante determinados tipos de ejercicio."),
        ("¿La creatina puede hacerme subir de peso?", "Puede aumentar el peso corporal debido, en parte, al agua almacenada en los músculos. La respuesta varía según la persona."),
        ("¿Cuánto tiempo tarda en hacer efecto?", "No existe un plazo universal. Los resultados dependen de factores individuales, la forma de uso y, cuando el objetivo es desarrollar músculo, el entrenamiento y la alimentación."),
        ("¿Cómo debo tomarla?", "Abre un sobre, mézclalo con 240–350 ml (8–12 oz) de agua, revuelve bien y bébelo. Sigue la porción indicada en la etiqueta de tu envase y no la excedas."),
        ("¿Puedo tomarla si tengo alguna condición médica?", "Si tienes una condición médica, tomas medicamentos, estás embarazada o amamantando, consulta con un profesional de salud antes de utilizarla."),
        ("¿Puedo pagar al recibir mi pedido?", "Sí. En Panamá ofrecemos pago contra entrega en la mayoría de zonas: no pagas por adelantado."),
        ("¿Cuánto cuesta y cuánto tarda el envío?", "El precio depende de la oferta que elijas en el formulario. El envío estándar es gratis; el extra rápido tiene un costo adicional de $2."),
    ]
    items = []
    for q, a in faqs:
        items.append(f'      <div class="faq-item"><button type="button" class="faq-q">{q} <i>+</i></button><div class="faq-a">{a}</div></div>')
    block = (
        '<section class="hl-section hl-cream">\n  <div class="shell">\n'
        '    <p class="hl-eyebrow">Preguntas frecuentes</p>\n'
        '    <h2 class="hl-title">Todo lo que debes saber</h2>\n'
        '    <div class="faq-list" id="faqList">\n'
        + "\n".join(items)
        + "\n    </div>\n  </div>\n</section>"
    )
    return re.sub(
        r'<section class="hl-section hl-cream">\s*<div class="shell">\s*<p class="hl-eyebrow">Preguntas frecuentes</p>.*?</section>',
        block,
        html,
        count=1,
        flags=re.S,
    )


def build_html() -> None:
    html = SRC_HTML.read_text(encoding="utf-8")
    html = html.replace("metabolae-ceylon-cinnamon", "yesnap-creatine-women")
    html = html.replace("metabolae-ceylon-cinnamon.css", "yesnap-creatine-women.css")
    html = html.replace('data-product="cinnamon-pa"', 'data-product="creatine-pa"')
    html = html.replace("cc-cinnamon-pa", "cc-creatine-pa")
    html = html.replace("cinnamon-timeline", "creatine-timeline")
    html = html.replace("Metabolae — Canela de Ceilán", "YESNAP Creatine for Women")
    html = html.replace("Metabolae Canela de Ceilán", "YESNAP Creatine for Women Peach Pout")
    html = html.replace("Metabolae Ceylon Cinnamon", "YESNAP Creatine for Women")
    html = html.replace("Metabolae — <em>Canela de Ceilán 7200 mg</em> con aceite MCT · 300 cápsulas blandas",
                        "YESNAP — <em>Creatine for Women</em> Peach Pout · 30 sobres · sabor durazno")
    html = html.replace(
        "<title>Metabolae Canela de Ceilán 7200 mg, with MCT Oil, 300 Softgels | CompraConfio Panamá</title>",
        "<title>YESNAP Creatine for Women Peach Pout — 30 sobres | CompraConfio Panamá</title>",
    )
    html = re.sub(
        r"<title>.*?</title>",
        "<title>YESNAP Creatine for Women Peach Pout — 30 sobres | CompraConfio Panamá</title>",
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="Creatina para mujeres YESNAP Peach Pout: 30 sobres, creatina monohidratada, colágeno y aminoácidos. Sabor durazno. Envío gratis y pago contra entrega en Panamá.">',
        html,
        count=1,
    )
    html = html.replace("/css/metabolae-ceylon-cinnamon.css?v=20261013g", f"/css/yesnap-creatine-women.css?v={V}")
    html = html.replace("/css/yesnap-creatine-women.css?v=20261013g", f"/css/yesnap-creatine-women.css?v={V}")

    if 'clarity.js' not in html:
        html = html.replace(
            "</head>",
            f'  <script src="/js/clarity.js?v=20261024" async></script>\n</head>',
        )

    body_tag = '<body data-country="PA"'
    if 'data-abandon-checkout' not in html:
        html = html.replace(
            body_tag,
            '<body data-country="PA" data-abandon-checkout="on" data-abandon-idle-minutes="5"',
        )

    html = replace_gallery(html)
    html = replace_voices(html)
    html = replace_timeline(html)
    html = replace_faq(html)

    html = re.sub(
        r'<ul class="hale-bullets">.*?</ul>',
        """<ul class="hale-bullets">
        <li>Trabaja por unos glúteos más redondos y definidos, sin cirugía</li>
        <li>Siéntete más segura con tu figura y con tu pareja</li>
        <li>Apoya tus objetivos de desarrollo muscular con una fórmula con creatina</li>
        <li>Incorpórala a tu rutina diaria siguiendo las instrucciones de la etiqueta</li>
        <li>30 sobres individuales · sabor durazno · fácil de mezclar con agua</li>
      </ul>""",
        html,
        count=1,
        flags=re.S,
    )

    html = html.replace('id="priceNow">$45', 'id="priceNow">$39')
    html = html.replace('id="priceWas">$59', 'id="priceWas">$69')
    html = html.replace('id="priceSave">Ahorra 24%', 'id="priceSave">Ahorra 43%')
    html = html.replace("1 Bolsa · 300 softgels · Envío gratis · Pago al recibir",
                        "1 Bolsa · 30 sobres · Envío gratis · Pago al recibir")
    html = html.replace(
        "<strong>Fórmula limpia · Sin gluten · Sin GMO · Sin soya</strong>",
        "<strong>Creatina 5 g · Colágeno · BCAA · Sabor durazno · 30 sobres</strong>",
    )
    html = html.replace("Ordenar ahora — Pago al recibir", "¡Quiero mi fórmula!")
    html = html.replace("Canela de Ceilán · 300 softgels", "Creatina para mujeres · 30 sobres")
    html = html.replace("7200 mg equivalente · MCT Oil", "11,700 mg por porción · sabor durazno")

    html = html.replace('strong id="stickyPrice">$45', 'strong id="stickyPrice">$39')
    html = html.replace('id="stickyLabel">1 Bolsa · 300 softgels', 'id="stickyLabel">1 Bolsa · 30 sobres')

    bundles_old = re.search(r'<span class="block-label">1\. Elige tu oferta</span>.*?</div>\s*\n\s*<div class="form-head">', html, re.S)
    if bundles_old:
        bundles = f"""<span class="block-label">1. Elige tu oferta</span>
        <div class="bundles">
          <label class="bundle bundle-option is-selected">
            <input type="radio" name="bundleOption" value="cc-creatine-pa-1" data-product-id="cc-creatine-pa-1" data-product-name="YESNAP Creatine for Women - 1 bolsa" data-price="39" data-old-price="69" data-save="43" data-label="1 Bolsa · 30 sobres" checked>
            <div class="bundle-card">
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>1 Bolsa</span>
                <span class="bundle-cost"><strong>$39</strong><del>$69</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot green"></span>30 sobres · uso según etiqueta</span>
              </div>
            </div>
          </label>
          <label class="bundle bundle-option">
            <input type="radio" name="bundleOption" value="cc-creatine-pa-2" data-product-id="cc-creatine-pa-2" data-product-name="YESNAP Creatine for Women - 2 bolsas" data-price="59" data-old-price="118" data-save="50" data-label="2 Bolsas · 60 sobres">
            <div class="bundle-card">
              <span class="bundle-flag">Más popular</span>
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>2 Bolsas</span>
                <span class="bundle-cost"><strong>$59</strong><del>$118</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot green"></span>60 sobres · Ahorra $19</span>
              </div>
            </div>
          </label>
          <label class="bundle bundle-option">
            <input type="radio" name="bundleOption" value="cc-creatine-pa-3" data-product-id="cc-creatine-pa-3" data-product-name="YESNAP Creatine for Women - 3 bolsas" data-price="79" data-old-price="177" data-save="55" data-label="3 Bolsas · 90 sobres">
            <div class="bundle-card">
              <span class="bundle-flag">Mejor valor</span>
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>3 Bolsas</span>
                <span class="bundle-cost"><strong>$79</strong><del>$177</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot green"></span>90 sobres · Ahorra $38</span>
              </div>
            </div>
          </label>
        </div>

        <div class="form-head">"""
        html = html[: bundles_old.start()] + bundles + html[bundles_old.end() :]

    html = html.replace('id="orderTotal" value="45"', 'id="orderTotal" value="39"')
    html = html.replace('id="sumSubtotal">$45', 'id="sumSubtotal">$39')
    html = html.replace('id="sumTotal">$45', 'id="sumTotal">$39')
    html = html.replace('300 cápsulas blandas · Envío gratis', '30 sobres · Envío gratis')

    if "abandoned-checkout.js" not in html:
        html = html.replace(
            '<script src="/js/main.js?v=20261025b" defer></script>',
            '<script src="/js/abandoned-checkout.js?v=20261025b" defer></script>\n<script src="/js/main.js?v=20261025b" defer></script>',
        )

    html = html.replace(
        "<h2>¿Estás cuidando tu salud metabólica?</h2>",
        "<h2>¿Quieres unos glúteos más redondos y atractivos?</h2>",
    )
    html = html.replace(
        "<p>Entre el trabajo y una rutina acelerada, mantener hábitos saludables no siempre es fácil: alimentación poco equilibrada, poca actividad físico y poco tiempo para cuidarte.</p>",
        "<p>Quieres mirarte al espejo y sentirte más sexy. Quieres lucir tus curvas con confianza y sentirte más segura con tu pareja. Conseguir la figura que deseas lleva tiempo, esfuerzo y constancia.</p>",
    )
    html = html.replace(
        "<b>Empieza a prestar más atención a tu bienestar — con información clara.</b>",
        "<b>No se trata solo de cómo te ves, sino de cómo te sientes cuando te miras al espejo.</b>",
    )

    html = html.replace(
        "<h2>Descubre los beneficios de la canela de Ceilán</h2>",
        "<h2>Tu rutina, tus curvas, tus objetivos</h2>",
    )
    html = html.replace(
        "<p>Información educativa. Este suplemento no sustituye medicamentos, tratamientos médicos ni una alimentación equilibrada.</p>",
        "<p>La creatina puede apoyar el rendimiento y el desarrollo muscular cuando se combina con entrenamiento. Los resultados varían.</p>",
    )

    html = html.replace("<h3>Apoyo metabólico</h3>", "<h3>Apoya el desarrollo muscular</h3>")
    html = html.replace("<h3>Sensibilidad a la insulina</h3>", "<h3>Apoya tu rendimiento</h3>")
    html = html.replace("<h3>Salud metabólica</h3>", "<h3>Complementa tu rutina fitness</h3>")
    html = html.replace("<h3>Canela de Ceilán</h3>", "<h3>Hazlo por ti</h3>")
    html = html.replace("<h3>Presentación concentrada</h3>", "<h3>Sobres listos para llevar</h3>")
    html = html.replace("<h3>Fácil de incorporar</h3>", "<h3>Sabor durazno</h3>")

    html = html.replace(
        "<h2 class=\"ingc__heading\">Conoce sus ingredientes</h2>",
        "<h2 class=\"ingc__heading\">Conoce los ingredientes de tu fórmula</h2>",
    )
    html = html.replace(
        '<p class="ingc__sub">Extracto de Ceilán · MCT · Cápsula blanda</p>',
        '<p class="ingc__sub">Creatina · Colágeno · BCAA · L-Glutamina</p>',
    )

    html = html.replace(">Canela de Ceilán<", ">Creatina monohidratada<")
    html = html.replace(">Aceite MCT<", ">Colágeno<")
    html = html.replace(">Gelatina<", ">BCAA<")
    html = html.replace(">Glicerina<", ">L-Glutamina<")

    html = html.replace(
        "<span class=\"ingc__card-title\">Extracto de canela de Ceilán (Cinnamomum verum)</span>",
        "<span class=\"ingc__card-title\">Creatina monohidratada</span>",
    )
    html = html.replace(
        "<span class=\"ingc__card-dose\">12:1 · 7,200 mg equivalente</span>",
        "<span class=\"ingc__card-dose\">5 g creatina por porción*</span>",
    )
    html = html.replace(
        "<span class=\"ingc__card-desc\">Extracto concentrado 12:1, equivalente a 7,200 mg de canela de Ceilán en bruto por porción.</span>",
        "<span class=\"ingc__card-desc\">Ingrediente estudiado por su papel en el rendimiento durante ejercicios breves e intensos. *Confirma cantidades en la etiqueta.</span>",
    )

    html = html.replace(
        "<span class=\"ingc__card-title\">Aceite MCT de coco</span>",
        "<span class=\"ingc__card-title\">Colágeno</span>",
    )
    html = html.replace(
        "<span class=\"ingc__card-dose\">Base líquida</span>",
        "<span class=\"ingc__card-dose\">Proteína nutricional</span>",
    )
    html = html.replace(
        "<span class=\"ingc__card-desc\">Aceite de triglicéridos de cadena media, utilizado como base líquida para la fórmula.</span>",
        "<span class=\"ingc__card-desc\">Proteína presente en distintas formulaciones de bienestar y belleza.</span>",
    )

    html = html.replace("<span class=\"ingc__card-title\">Gelatina</span>", "<span class=\"ingc__card-title\">BCAA</span>")
    html = html.replace(
        "<span class=\"ingc__card-dose\">Cápsula blanda</span>",
        "<span class=\"ingc__card-dose\">Aminoácidos ramificados</span>",
    )
    html = html.replace(
        "<span class=\"ingc__card-desc\">Material utilizado para formar la cápsula blanda.</span>",
        "<span class=\"ingc__card-desc\">Aminoácidos de cadena ramificada presentes en formulaciones deportivas.</span>",
    )

    html = html.replace("<span class=\"ingc__card-title\">Glicerina</span>", "<span class=\"ingc__card-title\">L-Glutamina</span>")
    html = html.replace(
        "<span class=\"ingc__card-dose\">Cubierta de la cápsula</span>",
        "<span class=\"ingc__card-dose\">Aminoácido</span>",
    )
    html = html.replace(
        "<span class=\"ingc__card-desc\">Componente de la cubierta de la cápsula.</span>",
        "<span class=\"ingc__card-desc\">Aminoácido presente de forma natural en el organismo. La fórmula puede incluir mioinositol, maca, ácido hialurónico o vitamina D3 según el envase.</span>",
    )

    html = html.replace(
        "<h2>Haz de tu bienestar una prioridad</h2>",
        "<h2>¡Es hora de ponerte como prioridad!</h2>",
    )
    html = html.replace(
        "<p class=\"safety-lead\">Incorpora Metabolae Ceylon Cinnamon de forma informada. Completa tus datos y confirma precio, dirección y pago contra entrega.</p>",
        "<p class=\"safety-lead\">Descubre YESNAP Creatine for Women y complementa tus objetivos de rendimiento y desarrollo muscular. Envío gratis y pago contra entrega en Panamá.</p>",
    )
    html = html.replace("¡Haz tu pedido ahora!", "¡Quiero mi creatina!")

    collapse_mode = re.search(
        r'<button type="button" class="collapse-btn">Modo de uso.*?</div>\s*</div>',
        html,
        re.S,
    )
    if collapse_mode:
        new_mode = """<button type="button" class="collapse-btn">¿Cómo tomar tu creatina? <i>+</i></button>
          <div class="collapse-body">
            <p><strong>Paso 1 — Abre un sobre</strong> individual. Si te cuesta rasgarlo, puedes utilizar unas tijeras.</p>
            <p><strong>Paso 2 — Mézclalo con agua:</strong> vierte el contenido en 240–350 ml (8–12 oz) de agua.</p>
            <p><strong>Paso 3 — Mezcla y disfruta:</strong> revuelve o agita bien hasta que se mezcle y bébelo enseguida.</p>
            <p><strong>Paso 4 — Sigue la etiqueta:</strong> toma la porción indicada en tu envase. No excedas la cantidad recomendada.</p>
            <p>Si estás embarazada, amamantando, tienes una condición médica o tomas medicamentos, consulta con un profesional de salud antes de utilizar este suplemento.</p>
          </div>
        </div>"""
        html = html[: collapse_mode.start()] + new_mode + html[collapse_mode.end() :]

    desc = re.search(r'<button type="button" class="collapse-btn">Descripción.*?</div>\s*</div>', html, re.S)
    if desc:
        new_desc = """<button type="button" class="collapse-btn">Descripción <i>+</i></button>
          <div class="collapse-body">
            <p><strong>YESNAP Creatine for Women (Peach Pout)</strong> es una fórmula en sobres con creatina monohidratada pensada para complementar la rutina de mujeres que entrenan fuerza y glúteos.</p>
            <p>Cada bolsa incluye <strong>30 sobres individuales</strong>. Sabor durazno. Mezcla con agua según las instrucciones del envase.</p>
            <p>Consulta siempre la etiqueta para verificar ingredientes, cantidades por porción e instrucciones de uso.</p>
          </div>
        </div>"""
        html = html[: desc.start()] + new_desc + html[desc.end() :]

    OUT_HTML.write_text(html, encoding="utf-8")
    print("wrote", OUT_HTML)


def main() -> None:
    fetch_images()
    build_css()
    build_html()


if __name__ == "__main__":
    main()
