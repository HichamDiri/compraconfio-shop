"""Create silk-skin-soap Panama landing (structure like thermal-wristband)."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
V = "20261008a"
IMG = ROOT / "images" / "silk-skin-soap"
THERMAL = ROOT / "images" / "thermal-wristband"


def gen_css() -> None:
    src = (ROOT / "css" / "thermal-wristband.css").read_text(encoding="utf-8")
    text = src.replace("Thermal Wristband Panamá", "SKT Piel de Seda — Panamá")
    text = text.replace("thermal-wristband", "silk-soap")
    text = text.replace("--wrist-", "--silk-")
    text = text.replace(".dot.wrist", ".dot.silk")
    for a, b in {
        "#ffedd5": "#fce7f3",
        "#ea580c": "#be185d",
        "#c2410c": "#9d174d",
        "#fffaf5": "#fffafb",
        "#fff7ed": "#fdf2f8",
        "#fed7aa": "#fbcfe8",
        "#fdba74": "#f9a8d4",
    }.items():
        text = text.replace(a, b)
    (ROOT / "css" / "silk-skin-soap.css").write_text(text, encoding="utf-8")


def _placeholder(label: str, sub: str, hue: tuple[int, int, int]) -> Image.Image:
    size = 1024
    im = Image.new("RGB", (size, size), (255, 250, 252))
    draw = ImageDraw.Draw(im)
    for y in range(size):
        t = y / size
        r = int(255 * (1 - t) + hue[0] * t)
        g = int(250 * (1 - t) + hue[1] * t)
        b = int(252 * (1 - t) + hue[2] * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    margin = 80
    draw.rounded_rectangle(
        (margin, margin + 120, size - margin, size - margin - 80),
        radius=48,
        fill=(255, 255, 255),
        outline=(236, 72, 153),
        width=4,
    )
    try:
        font_l = ImageFont.truetype("arial.ttf", 52)
        font_s = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font_l = ImageFont.load_default()
        font_s = font_l
    draw.text((size // 2, size // 2 - 20), label, fill=(157, 23, 77), anchor="mm", font=font_l)
    draw.text((size // 2, size // 2 + 50), sub, fill=(131, 24, 67), anchor="mm", font=font_s)
    return im


def save_im(im: Image.Image, base: str) -> None:
    t = im.copy()
    t.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    t.save(IMG / f"{base}.png", "PNG", optimize=True)
    t.save(IMG / f"{base}.webp", "WEBP", quality=84, method=6)
    th = im.copy()
    th.thumbnail((800, 800), Image.Resampling.LANCZOS)
    th.save(IMG / f"{base}-800.webp", "WEBP", quality=84, method=6)
    th2 = im.copy()
    th2.thumbnail((160, 160), Image.Resampling.LANCZOS)
    th2.save(IMG / f"{base}-thumb.webp", "WEBP", quality=80, method=6)


def gen_images() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    pink = (251, 207, 232)
    save_im(_placeholder("SKT® Piel de Seda™", "Niacinamida + Proteína de Seda", pink), "hero-product")
    save_im(_placeholder("¿Piel opaca o con manchas?", "Sol, tiempo y tono desigual", (254, 226, 226)), "story-problem")
    save_im(_placeholder("Limpia · Ilumina · Suaviza", "Tu rutina en la ducha", pink), "story-solution")
    save_im(_placeholder("4 pasos", "Moja · Espuma · Masajea · Enjuaga", pink), "how-to-demo")
    benefit_titles = [
        ("Aclara", "1"),
        ("Manchas", "2"),
        ("Ilumina", "3"),
        ("Unifica", "4"),
        ("Hidrata", "5"),
        ("Sedosa", "6"),
        ("Limpia", "7"),
        ("Aroma", "8"),
    ]
    for title, num in benefit_titles:
        save_im(_placeholder(f"Beneficio {num}", title, pink), f"benefit-{num}")
    for icon in ("icon-guarantee", "icon-shipping", "icon-cod"):
        for ext in ("png", "webp"):
            p = THERMAL / f"{icon}.{ext}"
            if p.exists():
                shutil.copy2(p, IMG / f"{icon}.{ext}")


def build_html() -> None:
    tpl = (ROOT / "thermal-wristband-panama.html").read_text(encoding="utf-8")
    text = tpl.replace("thermal-wristband", "silk-skin-soap")
    text = text.replace('data-product="silk-skin-soap"', 'data-product="silk-soap"')
    text = text.replace("cc-wristband-pa", "cc-silksoap-pa")
    text = text.replace("thermal-wristband-panama", "silk-skin-soap-panama")
    text = text.replace("silk-skin-soap.css?v=20261007a", f"silk-skin-soap.css?v={V}")
    text = re.sub(r"\?v=20261007[a-z]", f"?v={V}", text)

    # Remove extra hero slides — keep single product slide
    g0 = text.index('<section class="gallery"')
    g1 = text.index("</section>", g0) + len("</section>")
    gallery = f'''<section class="gallery" id="heroSection">
      <div class="gallery-stage" id="galleryTrack">
        <div class="slide">
          <picture>
            <source type="image/webp" media="(max-width: 960px)" srcset="/images/silk-skin-soap/hero-product-800.webp?v={V}">
            <source type="image/webp" srcset="/images/silk-skin-soap/hero-product.webp?v={V}">
            <img class="is-contain" src="/images/silk-skin-soap/hero-product.png?v={V}" alt="SKT Piel de Seda — Jabón de Niacinamida y Proteína de Seda" width="800" height="800" loading="eager" decoding="async" fetchpriority="high">
          </picture>
        </div>
      </div>
      <div class="gallery-dots" id="galleryDots" aria-hidden="true"></div>
      <div class="gallery-thumbs">
        <button type="button" class="thumb is-active" aria-label="Producto"><img src="/images/silk-skin-soap/hero-product-thumb.webp?v={V}" alt="" width="160" height="160" decoding="async"></button>
      </div>
    </section>'''
    text = text[:g0] + gallery + text[g1:]

    replacements = [
        (
            "<title>Muñequera Térmica con Masaje | CompraConfio Panamá — Pago Contra Entrega</title>",
            "<title>SKT® Piel de Seda™ — Jabón Niacinamida + Proteína de Seda | CompraConfio Panamá</title>",
        ),
        (
            'content="Muñequera térmica con masaje vibratorio: 3 niveles de calor, 3 modos de vibración, batería recargable y apagado automático a 15 min. Envío gratis y pago contra entrega en Panamá."',
            'content="Jabón SKT Piel de Seda con niacinamida y proteína de seda: ayuda a aclarar, iluminar y suavizar la piel. Envío gratis y pago contra entrega en Panamá."',
        ),
        ("Calor + masaje", "Niacinamida + seda"),
        ("100% inalámbrica", "Piel luminosa"),
        ("Calor + vibración · 15 min · Envío gratis · Pago al recibir · Garantía 30 días", "Aclara · Ilumina · Suaviza · Envío gratis · Pago al recibir · Garantía 30 días"),
        ("🔥 ¿Sufres de dolor o cansancio en las manos y muñecas?", "✨ Piel más clara, luminosa y sin manchas"),
        ("Muñequera Térmica con Masaje", "Jabón de Niacinamida + Proteína de Seda"),
        ("$75", "$65"),
        (
            "Calor relajante + masaje vibratorio para tus muñecas después de trabajar, usar el celular, el mouse o movimientos repetitivos. 3 niveles de calor · 3 modos de masaje · 15 min de apagado automático.",
            "SKT® Piel de Seda™ transforma tu rutina de baño. Niacinamida + Proteína de Seda ayudan a aclarar la piel, reducir la apariencia de manchas oscuras y unificar el tono, con sensación suave, fresca y sedosa.",
        ),
        ("✓ Calor relajante envolvente", "✓ Ayuda a aclarar la piel"),
        ("✓ Masaje vibratorio con 2 motores", "✓ Ayuda a reducir manchas oscuras"),
        ("✓ 3 niveles de calor (48°C · 53°C · 58°C)", "✓ Ilumina y unifica el tono"),
        ("✓ Batería recargable — sin cables", "✓ Suaviza e hidrata"),
        ("✓ Correa ajustable — izquierda o derecha", "✓ Sensación sedosa al tacto"),
        ("Quiero la mía", "Quiero probarlo ahora"),
        ("Calor + masaje · Envío gratis", "Niacinamida + seda · Envío gratis"),
        ('data-old-price="75"', 'data-old-price="65"'),
        ("Muñequera Térmica con Masaje - 1 unidad", "SKT Piel de Seda - Jabón 1 unidad"),
        ("Muñequera Térmica con Masaje - 2 unidades", "SKT Piel de Seda - Jabón 2 unidades"),
        ("Calor + vibración · batería recargable", "Niacinamida + proteína de seda"),
        ("1 Unidad", "1 Jabón"),
        ("2 Unidades", "2 Jabones"),
        ("$45", "$39"),
        ('data-price="45"', 'data-price="39"'),
        ('value="45"', 'value="39"'),
        ("$45</strong>", "$39</strong>"),
        ("Muñequera Térmica con Masaje", "SKT® Piel de Seda™ — Jabón"),
    ]
    for a, b in replacements:
        text = text.replace(a, b)

    # Story
    story0 = text.index('<section class="story-flow"')
    story1 = text.index('<section class="hl-section hl-warm" id="beneficios">')
    story = f'''<section class="story-flow" aria-label="Cuidado de la piel">

  <section class="feature story-step">
    <div class="feature-inner">
      <div class="feature-media feature-media--square">
        <picture><source type="image/webp" srcset="/images/silk-skin-soap/story-problem.webp?v={V}"><img src="/images/silk-skin-soap/story-problem.png?v={V}" alt="Piel opaca, oscura o con manchas y tono desigual" width="800" height="800" loading="lazy" decoding="async"></picture>
      </div>
      <div class="feature-copy">
        <h2>¿Piel opaca, oscura o con manchas?</h2>
        <p>El sol, el paso del tiempo y otros factores pueden hacer que tu piel pierda luminosidad y luzca con <strong>manchas, tono desigual y una apariencia apagada</strong>.</p>
        <p><strong>¿Te gustaría recuperar una piel más clara, luminosa y uniforme?</strong></p>
      </div>
    </div>
  </section>

  <section class="feature story-step is-reversed">
    <div class="feature-inner">
      <div class="feature-media feature-media--square">
        <picture><source type="image/webp" srcset="/images/silk-skin-soap/story-solution.webp?v={V}"><img src="/images/silk-skin-soap/story-solution.png?v={V}" alt="Jabón de Niacinamida y Proteína de Seda — limpia, ilumina y suaviza" width="800" height="800" loading="lazy" decoding="async"></picture>
      </div>
      <div class="feature-copy">
        <h2>Conoce el Jabón de Niacinamida + Proteína de Seda</h2>
        <p>Una forma sencilla de cuidar la apariencia de tu piel mientras te duchas.</p>
        <p>Su fórmula ayuda a <strong>aclarar la piel, reducir la apariencia de manchas oscuras e iluminar el tono</strong>, mientras deja una sensación de suavidad, hidratación y piel sedosa.</p>
        <p><strong>🧼 Limpia + Ilumina + Suaviza — todo en un solo jabón.</strong></p>
        <button type="button" class="text-link js-open-order">Quiero probarlo ahora</button>
      </div>
    </div>
  </section>

</section>

<section class="hl-section hl-warm" id="beneficios">'''
    text = text[:story0] + story + text[story1:]

    benefits = [
        ("🤍 Ayuda a aclarar la piel", "Ayuda a mejorar la apariencia de una piel oscura o apagada, para un aspecto más claro y luminoso."),
        ("✨ Ayuda a reducir las manchas", "Ayuda a mejorar la apariencia de manchas oscuras y zonas con tono desigual."),
        ("🌟 Ilumina la piel", "Ayuda a devolver una apariencia más fresca, luminosa y radiante."),
        ("🎯 Ayuda a unificar el tono", "Contribuye a una apariencia más uniforme y equilibrada."),
        ("💧 Hidrata y suaviza", "Deja la piel con sensación de hidratación, suavidad y confort."),
        ("🕊️ Piel más sedosa", "La proteína de seda ayuda a una sensación suave, tersa y sedosa al tacto."),
        ("🫧 Limpia la piel", "Ayuda a eliminar suciedad, sudor y exceso de grasa con sensación de frescura."),
        ("🌸 Aroma agradable", "Experiencia de limpieza fresca con un delicado aroma."),
    ]
    b_start = text.index('<div class="mech-head mech-head--solo">', text.index('id="beneficios"'))
    b_end = text.index('<section class="section how-to-section">')
    head = '''    <div class="mech-head mech-head--solo">
      <h2>Todo lo que tu piel puede disfrutar en un solo jabón</h2>
      <p>Principales beneficios</p>
    </div>

    <div class="mech-track" id="reasonTrack">'''
    cards = ""
    for i, (title, body) in enumerate(benefits, start=1):
        active = " is-active" if i == 1 else ""
        cards += f'''
      <button type="button" class="mech-card{active}">
        <picture><source type="image/webp" srcset="/images/silk-skin-soap/benefit-{i}.webp?v={V}"><img src="/images/silk-skin-soap/benefit-{i}.png?v={V}" alt="{title}" width="800" height="800" loading="lazy" decoding="async"></picture>
        <h3>{title}</h3>
        <p>{body}</p>
      </button>'''
    text = text[:b_start] + head + cards + "\n    </div>\n  </div>\n</section>\n\n" + text[b_end:]

    # How-to
    h0 = text.index('<section class="section how-to-section">')
    h1 = text.index('<section class="hl-section hl-warm" id="resenas">')
    how = f'''<section class="section how-to-section">
  <div class="shell">
    <div class="feature-inner how-to-inner">
      <div class="feature-media feature-media--square">
        <picture><source type="image/webp" srcset="/images/silk-skin-soap/how-to-demo.webp?v={V}"><img src="/images/silk-skin-soap/how-to-demo.png?v={V}" alt="Cómo usar el jabón — moja, espuma, masajea y enjuaga" width="800" height="800" loading="lazy" decoding="async"></picture>
      </div>
      <div class="feature-copy">
        <h2>Tu rutina de cuidado en 4 simples pasos</h2>
        <div class="steps-panel">
          <ol>
            <li><strong>01 — Moja.</strong> Humedece tu piel con agua.</li>
            <li><strong>02 — Haz espuma.</strong> Frota el jabón entre tus manos o con una esponja hasta crear abundante espuma.</li>
            <li><strong>03 — Masajea.</strong> Aplica la espuma y masajea suavemente con movimientos circulares.</li>
            <li><strong>04 — Enjuaga.</strong> Enjuaga completamente y seca suavemente.</li>
          </ol>
          <p class="how-to-note"><strong>Úsalo diariamente</strong> para mantener una piel limpia, suave y de apariencia más luminosa.</p>
        </div>
        <button type="button" class="btn-order js-open-order">Quiero probarlo ahora</button>
      </div>
    </div>
  </div>
</section>

<section class="hl-section hl-cream" id="ingredientes">
  <div class="shell">
    <div class="mech-head mech-head--solo">
      <h2>Una combinación pensada para el cuidado diario</h2>
    </div>
    <div class="spec-grid">
      <div class="spec-item"><strong>✨ Niacinamida</strong><span>Ayuda a mejorar la apariencia del tono y aportar luminosidad.</span></div>
      <div class="spec-item"><strong>🕊️ Proteína de seda</strong><span>Sensación de suavidad, tersura y sedosidad después de la limpieza.</span></div>
      <div class="spec-item"><strong>🌹 Rosa</strong><span>Experiencia fresca con delicado aroma floral.</span></div>
      <div class="spec-item"><strong>🧼 Rutina simple</strong><span>Niacinamida + proteína de seda + limpieza diaria en un solo jabón.</span></div>
    </div>
  </div>
</section>

<section class="hl-section hl-warm" id="resenas">'''
    text = text[:h0] + how + text[h1 + len('<section class="hl-section hl-warm" id="resenas">'):]

    # Reviews
    text = text.replace(
        "<h2>Lo que dicen quienes lo han usado</h2>",
        "<h2>Descubre por qué tantas mujeres lo incorporan a su rutina</h2>",
    )
    r0 = text.index('<div class="review-grid gluta-review-grid">')
    r1 = text.index("</div></div>", r0) + len("</div>")
    reviews = '''    <div class="review-grid gluta-review-grid">
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Me encanta cómo queda mi piel después de usarlo.”</strong> Se siente mucho más suave y limpia.</p>
        <cite>— Cliente verificada</cite>
      </article>
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Mi piel se siente más suave y se ve mucho más luminosa.”</strong></p>
        <cite>— Cliente verificada</cite>
      </article>
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Tiene un aroma muy agradable”</strong> y deja una sensación súper bonita en la piel.</p>
        <cite>— Cliente verificada</cite>
      </article>
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Muy fácil de usar.”</strong> Simplemente lo agregué a mi rutina de baño.</p>
        <cite>— Cliente verificada</cite>
      </article>
    </div>'''
    text = text[:r0] + reviews + text[r1:]
    note = '''    <p class="gluta-review-note">Tu piel también merece sentirse y verse increíble.</p>
    <p class="notice notice--center"><strong>🚚 Envío GRATIS · 💵 Pago contra entrega</strong></p>
    <div class="section-cta">
      <button type="button" class="btn-order js-open-order">Quiero mi jabón ahora</button>
    </div>'''
    text = text.replace(
        "</div></div>\n  </div>\n</section>\n\n<section class=\"section\" id=\"faq\">",
        "</div>\n" + note + "\n  </div>\n</section>\n\n<section class=\"section\" id=\"faq\">",
        1,
    )

    # FAQ
    faqs = [
        ("¿Puedo usar el jabón todos los días?", "Sí. Puedes incorporarlo a tu rutina diaria de limpieza siguiendo las instrucciones de uso."),
        ("¿Ayuda a reducir las manchas oscuras?", "Sí. Su fórmula está diseñada para ayudar a mejorar la apariencia de manchas oscuras y zonas con tono desigual."),
        ("¿Ayuda a aclarar la piel?", "Sí. La niacinamida ayuda a mejorar la apariencia de una piel apagada y un tono más luminoso."),
        ("¿Cuándo comenzaré a notar resultados?", "Los resultados pueden variar. Recomendamos uso constante como parte de tu rutina."),
        ("¿Puedo utilizarlo en el rostro?", "Úsalo según las indicaciones del fabricante en el empaque. Si es apto para rostro, aplícalo con cuidado; si no, úsalo en el cuerpo."),
        ("¿Es adecuado para todo tipo de piel?", "Está diseñado para limpieza diaria. Si tienes piel sensible, haz una prueba en una zona pequeña primero."),
        ("¿Deja la piel seca?", "Está formulado para dejar sensación de suavidad y confort después del enjuague."),
        ("¿Tiene aroma?", "Sí. Ingredientes de rosa que aportan una experiencia aromática agradable."),
        ("¿Cómo debo conservarlo?", "Colócalo en un lugar seco y deja que se seque entre usos para prolongar su duración."),
        ("¿Qué hago si mi piel se irrita?", "Suspende el uso si aparece irritación. Si persiste, consulta con un profesional de la salud."),
        ("¿Cómo recibo mi pedido?", "Ofrecemos <strong>pago contra entrega</strong>. Pagas en efectivo al recibir."),
        ("¿El envío tiene costo?", "No. El envío es <strong>GRATIS</strong> a toda Panamá."),
    ]
    f0 = text.index('<section class="section" id="faq">')
    f1 = text.index("</section>\n\n<footer", f0)
    faq_html = '<section class="section" id="faq">\n  <div class="shell">\n    <h2 class="section-title">❓ Preguntas frecuentes</h2>\n    <div class="faq collapse-group">\n'
    for q, a in faqs:
        faq_html += f'      <div class="collapse">\n        <button type="button" class="collapse-btn">{q} <i>+</i></button>\n        <div class="collapse-body">{a}</div>\n      </div>\n'
    faq_html += "    </div>\n  </div>\n</section>\n\n"
    text = text[:f0] + faq_html + text[f1:]

    text = text.replace('class="dot wrist"', 'class="dot silk"')
    text = text.replace("lazyLoadGif(document.getElementById('howToDemo'));\n\n", "")

    (ROOT / "silk-skin-soap-panama.html").write_text(text, encoding="utf-8")


def main() -> None:
    gen_css()
    gen_images()
    build_html()
    print("built silk-skin-soap-panama")


if __name__ == "__main__":
    main()
