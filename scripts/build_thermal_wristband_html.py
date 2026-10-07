"""Generate thermal-wristband-panama.html from dumpling template."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = "20261007a"
src = (ROOT / "dumpling-maker-set-panama.html").read_text(encoding="utf-8")

pairs = [
    ("Set para Cortar y Moldear Masa", "Muñequera Térmica con Masaje"),
    ("dumpling-maker-set", "thermal-wristband"),
    ("dumpling-maker", "thermal-wristband"),
    ("data-product=\"thermal-wristband\"", "data-product=\"thermal-wristband\""),
    ("cc-dumpling-pa", "cc-wristband-pa"),
    ("dumpling-maker-set-panama", "thermal-wristband-panama"),
    (".dot.dumpling", ".dot.wrist"),
    ("🥟 Prepara empanadas perfectas sin pasar horas en la cocina", "🔥 ¿Sufres de dolor o cansancio en las manos y muñecas?"),
    (
        "Corta, rellena y sella tus empanadas en pocos pasos. Haz empanadas, pastelitos, raviolis, dumplings y otras recetas rellenas de forma más rápida, sencilla y uniforme.",
        "Calor relajante + masaje vibratorio para tus muñecas después de trabajar, usar el celular, el mouse o movimientos repetitivos. 3 niveles de calor · 3 modos de masaje · 15 min de apagado automático.",
    ),
    ("✓ Corta la masa con facilidad", "✓ Calor relajante envolvente"),
    ("✓ Ayuda a conseguir formas uniformes", "✓ Masaje vibratorio con 2 motores"),
    ("✓ Rellena y sella en pocos pasos", "✓ 3 niveles de calor (48°C · 53°C · 58°C)"),
    ("✓ Ideal para preparar varias piezas", "✓ Batería recargable — sin cables"),
    ("✓ Reutilizable y fácil de limpiar", "✓ Correa ajustable — izquierda o derecha"),
    ("Corta · Rellena · Sella · Envío gratis · Pago al recibir · Garantía 30 días", "Calor + vibración · 15 min · Envío gratis · Pago al recibir · Garantía 30 días"),
    ("Acero inoxidable", "Calor + masaje"),
    ("Cortador + molde 2 en 1", "100% inalámbrica"),
    ("Ordena ahora", "Quiero la mía"),
    ("1 Set", "1 Unidad"),
    ("2 Sets", "2 Unidades"),
    ("3 Sets", "3 Unidades"),
    ("Set para Cortar y Moldear Masa - 1 set", "Muñequera Térmica con Masaje - 1 unidad"),
    ("Set para Cortar y Moldear Masa - 2 sets", "Muñequera Térmica con Masaje - 2 unidades"),
    ("Set para Cortar y Moldear Masa - 3 sets", "Muñequera Térmica con Masaje - 3 unidades"),
    ("Cortador + molde acero inoxidable", "Calor + vibración · batería recargable"),
    ("Ideal para regalo o cocinar en familia", "Ideal para regalar o tener una de repuesto"),
    ("Máximo ahorro · comparte o regala", "Mejor precio por unidad"),
    ("Acero inoxidable · Envío gratis", "Recargable · Envío gratis"),
    ("Prepara las tuyas — Ordena ahora", "Dale descanso a tus muñecas — Ordena ahora"),
    ("$60", "$65"),
    ("$120", "$130"),
    ("$180", "$195"),
    ("Ahorra 35%", "Ahorra 40%"),
    ('data-old-price="60"', 'data-old-price="65"'),
    ('data-save="35"', 'data-save="40"'),
    ('data-old-price="120"', 'data-old-price="130"'),
    ('data-save="55"', 'data-save="58"'),
    ('data-old-price="180"', 'data-old-price="195"'),
    ('data-save="62"', 'data-save="65"'),
]

for a, b in pairs:
    src = src.replace(a, b)

# Meta description
src = src.replace(
    'content="Set para cortar y moldear masa: corta, rellena y sella empanadas en pocos pasos. Acero inoxidable, manual y reutilizable. Envío gratis y pago contra entrega en Panamá."',
    'content="Muñequera térmica con masaje vibratorio: 3 niveles de calor, 3 modos de vibración, batería recargable y apagado automático a 15 min. Envío gratis y pago contra entrega en Panamá."',
)

# Version query strings
import re

src = re.sub(r"\?v=20260925[a-z]", f"?v={V}", src)
src = re.sub(r"\?v=20260925f", f"?v={V}", src)
src = src.replace("thermal-wristband.css?v=20260925a", f"thermal-wristband.css?v={V}")

# Single gallery slide + thumb (remove extra slides)
gallery_start = src.index('<section class="gallery"')
gallery_end = src.index("</section>", gallery_start) + len("</section>")
single_gallery = f'''<section class="gallery" id="heroSection">
      <div class="gallery-stage" id="galleryTrack">
        <div class="slide">
          <picture>
            <source type="image/webp" media="(max-width: 960px)" srcset="/images/thermal-wristband/hero-product-800.webp?v={V}">
            <source type="image/webp" srcset="/images/thermal-wristband/hero-product.webp?v={V}">
            <img class="is-contain" src="/images/thermal-wristband/hero-product.png?v={V}" alt="Muñequera térmica eléctrica con masaje vibratorio y pantalla digital" width="800" height="800" loading="eager" decoding="async" fetchpriority="high">
          </picture>
        </div>
      </div>
      <div class="gallery-dots" id="galleryDots" aria-hidden="true"></div>
      <div class="gallery-thumbs">
        <button type="button" class="thumb is-active" aria-label="Producto"><img src="/images/thermal-wristband/hero-product-thumb.webp?v={V}" alt="" width="160" height="160" decoding="async"></button>
      </div>
    </section>'''
src = src[:gallery_start] + single_gallery + src[gallery_end:]

# Story section
story_start = src.index('<section class="story-flow"')
story_end = src.index("</section>\n\n<section class=\"hl-section hl-warm\" id=\"beneficios\">")
story = f'''<section class="story-flow" aria-label="Descanso para tus muñecas">

  <section class="feature story-step">
    <div class="feature-inner">
      <div class="feature-media feature-media--square">
        <picture><source type="image/webp" srcset="/images/thermal-wristband/story-problem.webp?v={V}"><img src="/images/thermal-wristband/story-problem.png?v={V}" alt="Manos y muñecas cansadas después de trabajo y pantallas" width="800" height="800" loading="lazy" decoding="async"></picture>
      </div>
      <div class="feature-copy">
        <h2>¿Sufres de dolor en las manos y muñecas?</h2>
        <p>¿Tus manos y muñecas se sienten <strong>cansadas, tensas o adoloridas</strong> después de trabajar, usar el celular o hacer movimientos repetitivos?</p>
        <p>No tienes que seguir soportando esa sensación durante todo el día.</p>
        <p><strong>Tus manos trabajan por ti todos los días. Ahora es momento de cuidarlas.</strong></p>
      </div>
    </div>
  </section>

  <section class="feature story-step is-reversed">
    <div class="feature-inner">
      <div class="feature-media feature-media--square">
        <img class="story-solution-demo" id="storySolutionDemo" src="/images/thermal-wristband/story-solution-poster.webp?v={V}" data-animate="/images/thermal-wristband/story-solution.webp?v={V}" alt="Muñequera térmica con calor y masaje vibratorio en uso" width="800" height="800" loading="lazy" decoding="async">
      </div>
      <div class="feature-copy">
        <h2>Dale a tus muñecas el descanso que necesitan</h2>
        <p>Combina <strong>calor relajante + masaje vibratorio</strong> para ayudarte a relajar la tensión y disfrutar de una sensación reconfortante en solo <strong>15 minutos</strong>.</p>
        <p><strong>Póntela. Enciéndela. Relájate.</strong></p>
        <p>Una pequeña pausa para tus muñecas puede cambiar cómo termina tu día.</p>
        <button type="button" class="text-link js-open-order">Quiero la mía</button>
      </div>
    </div>
  </section>

</section>

<section class="hl-section hl-warm" id="beneficios">'''
src = src[:story_start] + story + src[story_end + len("</section>\n\n<section class=\"hl-section hl-warm\" id=\"beneficios\">"):]

benefits_head = '''    <div class="mech-head mech-head--solo">
      <h2>¡Recupera la sensación de comodidad en tus muñecas!</h2>
      <p>Principales beneficios</p>
    </div>

    <div class="mech-track" id="reasonTrack">'''
benefits_cards = [
    ("1", "🔥 Combate la sensación de tensión", "El calor envolvente ayuda a relajar rigidez, cansancio y tensión después de un largo día."),
    ("2", "〰️ Masaje que relaja", "Dos motores de vibración proporcionan un masaje suave para liberar tensión acumulada."),
    ("3", "😣 Deja atrás las muñecas agotadas", "Ideal después de horas con mouse, teclado, celular o movimientos repetitivos."),
    ("4", "⚡ Relájate en 15 minutos", "Sesión rápida de calor + vibración cuando tus muñecas necesitan un descanso."),
    ("5", "🔥 Elige la intensidad que quieras", "3 niveles de calor: 48°C · 53°C · 58°C."),
    ("6", "🔋 Sin cables", "Batería recargable de 2.000 mAh — úsala donde quieras, sin enchufe."),
    ("7", "🤲 Ajuste cómodo", "Correa ajustable para distintos tamaños; izquierda o derecha."),
]
cards_html = ""
for i, (num, title, body) in enumerate(benefits_cards):
    active = " is-active" if i == 0 else ""
    cards_html += f'''
      <button type="button" class="mech-card{active}">
        <picture><source type="image/webp" srcset="/images/thermal-wristband/benefit-{num}.webp?v={V}"><img src="/images/thermal-wristband/benefit-{num}.png?v={V}" alt="{title}" width="800" height="800" loading="lazy" decoding="async"></picture>
        <h3>{title}</h3>
        <p>{body}</p>
      </button>'''
benefits_end = src.index('<section class="section how-to-section">')
benefits_start = src.index('<div class="mech-head mech-head--solo">', src.index('id="beneficios"'))
src = src[:benefits_start] + benefits_head + cards_html + "\n    </div>\n  </div>\n</section>\n\n" + src[benefits_end:]

# How-to
how_start = src.index('<section class="section how-to-section">')
how_end = src.index('<section class="hl-section hl-warm" id="resenas">')
how = f'''<section class="section how-to-section">
  <div class="shell">
    <div class="feature-inner how-to-inner">
      <div class="feature-media feature-media--square">
        <picture><source type="image/webp" srcset="/images/thermal-wristband/how-to-demo.webp?v={V}"><img src="/images/thermal-wristband/how-to-demo.png?v={V}" alt="Cómo usar la muñequera térmica — coloca, elige modo y relájate" width="800" height="800" loading="lazy" decoding="async"></picture>
      </div>
      <div class="feature-copy">
        <h2>¡3 pasos y listo!</h2>
        <div class="steps-panel">
          <ol>
            <li><strong>01 — Colócala.</strong> Envuelve la muñequera alrededor de tu muñeca y ajusta la correa hasta sentirla cómoda.</li>
            <li><strong>02 — Elige.</strong> Selecciona tu nivel de calor y el modo de vibración que prefieras.</li>
            <li><strong>03 — Relájate.</strong> Disfruta de 15 minutos de calor y masaje mientras descansas.</li>
          </ol>
          <p class="how-to-note"><strong>Se apaga automáticamente</strong> al terminar la sesión. Así de fácil.</p>
        </div>
        <button type="button" class="btn-order js-open-order">Quiero la mía</button>
      </div>
    </div>
  </div>
</section>

<section class="hl-section hl-cream" id="tecnologia">
  <div class="shell">
    <div class="mech-head mech-head--solo">
      <h2>Tecnología diseñada para tus momentos de descanso</h2>
    </div>
    <div class="spec-grid">
      <div class="spec-item"><strong>🔥 3 niveles de calor</strong><span>48°C · 53°C · 58°C</span></div>
      <div class="spec-item"><strong>〰️ Doble motor</strong><span>Masaje vibratorio suave</span></div>
      <div class="spec-item"><strong>🔋 Batería 2.000 mAh</strong><span>Aprox. 4–5 sesiones por carga</span></div>
      <div class="spec-item"><strong>⏱️ Temporizador</strong><span>Apagado automático a 15 min</span></div>
      <div class="spec-item"><strong>🤲 Diseño ajustable</strong><span>Muñeca izquierda o derecha</span></div>
      <div class="spec-item"><strong>🧸 Material suave</strong><span>Interior flexible y cómodo</span></div>
    </div>
    <p class="notice notice--center" style="margin-top:1.5rem"><em>No es un producto médico. Bienestar: calor y masaje para mayor comodidad y relajación.</em></p>
  </div>
</section>

<section class="hl-section hl-warm" id="resenas">'''
src = src[:how_start] + how + src[how_end + len('<section class="hl-section hl-warm" id="resenas">'):]

# Reviews
rev_start = src.index('<div class="review-grid gluta-review-grid">')
rev_end = src.index("</div>", src.index('<p class="gluta-review-note">'))
reviews = '''    <div class="review-grid gluta-review-grid">
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“¡El calor es increíble!”</strong> Se calienta rápidamente y la sensación es muy agradable. La uso después de trabajar cuando siento las muñecas cansadas.</p>
        <cite>— Cliente verificado</cite>
      </article>
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Muy cómoda y fácil de usar”</strong> Puedo ajustar la correa y utilizarla en cualquiera de las dos muñecas. Es muy práctica.</p>
        <cite>— Cliente verificado</cite>
      </article>
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Perfecta después de un día largo”</strong> La uso por la noche mientras descanso. El calor y la vibración hacen un momento muy relajante.</p>
        <cite>— Cliente verificado</cite>
      </article>
      <article class="review-card">
        <div class="stars">★★★★★</div>
        <p><strong>“Me encanta que sea inalámbrica”</strong> No tengo que estar cerca de un enchufe. Puedo usarla en el sofá.</p>
        <cite>— Cliente verificado</cite>
      </article>
    </div>'''
src = src[:rev_start] + reviews + src[rev_end:]
src = src.replace(
    "Un set práctico que simplifica la preparación de tus recetas favoritas.",
    "Miles de momentos de relajación, una sola muñequera.",
)

# FAQ
faq_start = src.index('<section class="section" id="faq">')
faq_end = src.index("</section>\n\n<footer", faq_start)
faqs = [
    ("¿Puedo utilizarla en ambas muñecas?", "Sí. Su diseño ajustable permite utilizarla tanto en la <strong>muñeca izquierda como en la derecha</strong>."),
    ("¿Cuántos niveles de calor tiene?", "Cuenta con <strong>3 niveles de temperatura: 48°C, 53°C y 58°C</strong>."),
    ("¿Cuántos modos de masaje tiene?", "Cuenta con <strong>3 modos de vibración</strong> y dos motores incorporados."),
    ("¿Cuánto dura cada sesión?", "El temporizador automático está configurado para <strong>15 minutos</strong>."),
    ("¿Necesita estar conectada a la corriente?", "No. Batería recargable de <strong>2.000 mAh</strong> — úsala sin cables."),
    ("¿Cuánto dura la batería?", "Una carga completa permite aproximadamente <strong>4–5 sesiones</strong>, según calor y vibración."),
    ("¿Puedo usarla mientras trabajo?", "Sí, en actividades tranquilas como trabajar, descansar o ver televisión, si no interfiere con lo que haces."),
    ("¿Se adapta a diferentes tamaños?", "Sí. Su cierre ajustable se adapta a distintos tamaños de muñeca."),
    ("¿Puedo dormir con ella puesta?", "No recomendamos usarla dormido. Está diseñada para sesiones de <strong>15 minutos</strong>."),
    ("¿Es un producto médico?", "No. Es bienestar: <strong>calor y masaje vibratorio</strong> para comodidad y relajación."),
    ("¿Cómo se limpia?", "Con un paño ligeramente húmedo. <strong>No la sumerjas en agua</strong> ni la laves directamente."),
    ("¿Cómo recibo mi pedido?", "Ofrecemos <strong>pago contra entrega</strong>. Pagas en efectivo al recibir."),
    ("¿El envío tiene costo?", "No. El envío es <strong>GRATIS</strong> a toda Panamá."),
]
faq_html = '<section class="section" id="faq">\n  <div class="shell">\n    <h2 class="section-title">❓ Preguntas frecuentes</h2>\n    <div class="faq collapse-group">\n'
for q, a in faqs:
    faq_html += f'      <div class="collapse">\n        <button type="button" class="collapse-btn">{q} <i>+</i></button>\n        <div class="collapse-body">{a}</div>\n      </div>\n'
faq_html += "    </div>\n  </div>\n</section>\n\n"
src = src[:faq_start] + faq_html + src[faq_end:]

# Add spec-grid styles inline in page? Check if product.css has spec-grid - grep
out = ROOT / "thermal-wristband-panama.html"
out.write_text(src, encoding="utf-8")
print("wrote", out)
