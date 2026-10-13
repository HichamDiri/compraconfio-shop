"""Patch metabolae-ceylon-cinnamon-panama.html from nattokinase copy."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "metabolae-ceylon-cinnamon-panama.html"
html = path.read_text(encoding="utf-8")
img = "/images/metabolae-ceylon-cinnamon"
v = "20261013a"

head_old = """  <title>Nattokinasa 10,000 FU — Circulación y Salud del Corazón | CompraConfio Panamá</title>
  <meta name="description" content="Nattokinasa 10,000 FU por porción con CoQ10, bromelina, cúrcuma, extracto de ajo envejecido y extracto de corteza de pino. 240 cápsulas vegetarianas. Envío gratis y pago contra entrega en Panamá.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/product.css?v=20260811a">
  <link rel="stylesheet" href="/css/nattokinase-hale.css?v=20261012b">
</head>
<body data-country="PA" data-lang="es" data-brand="compraconfio" data-product="natto-pa" data-fb-pixel-id="1398615545550804" data-snap-pixel="off" data-thankyou="/thank-you-compraconfio-panama.html">"""

head_new = f"""  <title>Metabolae Ceylon Cinnamon 7200 mg + MCT Oil — 300 Softgels | CompraConfio Panamá</title>
  <meta name="description" content="Metabolae Ceylon Cinnamon 7200 mg con aceite MCT. Canela de Ceilán (Cinnamomum verum), 300 softgels. Apoya tu rutina de bienestar metabólico. Envío gratis y pago contra entrega en Panamá.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/product.css?v=20260811a">
  <link rel="stylesheet" href="/css/metabolae-ceylon-cinnamon.css?v={v}">
</head>
<body data-country="PA" data-lang="es" data-brand="compraconfio" data-product="cinnamon-pa" data-fb-pixel-id="1398615545550804" data-snap-pixel="off" data-thankyou="/thank-you-compraconfio-panama.html">"""

html = html.replace(head_old, head_new)

announce = """    <span>Envío gratis y pago contra entrega en toda Panamá</span>
    <span>Garantía de 90 días</span>
    <span>Canela de Ceilán · 300 softgels</span>
    <span>7200 mg equivalente · MCT Oil</span>
    <span>Envío gratis y pago contra entrega en toda Panamá</span>
    <span>Garantía de 90 días</span>
    <span>Canela de Ceilán · 300 softgels</span>"""
html = re.sub(
    r"<div class=\"announce-track\">.*?</div>",
    f'<div class="announce-track">\n    {announce}\n  </div>',
    html,
    count=1,
    flags=re.S,
)

gallery = f"""
    <section class="gallery" id="heroSection">
      <div class="gallery-stage" id="galleryTrack">
        <div class="slide">
          <img class="is-contain" src="{img}/hero-product.jpg?v={v}" alt="Metabolae Ceylon Cinnamon 7200 mg con MCT Oil — 300 softgels" width="1024" height="1024" loading="eager" decoding="async">
        </div>
        <div class="slide">
          <img class="is-contain" src="{img}/hero-softgels.jpg?v={v}" alt="Softgels de canela de Ceilán — presentación Metabolae" width="1024" height="1024" loading="lazy" decoding="async">
        </div>
        <div class="slide">
          <img class="is-contain" src="{img}/hero-ingredients.jpg?v={v}" alt="Canela de Ceilán, coco y softgels — ingredientes" width="1024" height="1024" loading="lazy" decoding="async">
        </div>
        <div class="slide">
          <img class="is-contain" src="{img}/hero-label.jpg?v={v}" alt="Etiqueta Metabolae — extracto de canela de Ceilán con aceite MCT" width="1024" height="1024" loading="lazy" decoding="async">
        </div>
        <div class="slide">
          <img class="is-contain" src="{img}/hero-mct.jpg?v={v}" alt="Fórmula con aceite MCT para absorción" width="1024" height="1024" loading="lazy" decoding="async">
        </div>
      </div>
      <div class="gallery-dots" id="galleryDots" aria-hidden="true"></div>
      <div class="gallery-thumbs">
        <button type="button" class="thumb is-active" aria-label="Producto"><img src="{img}/hero-product.jpg?v={v}" alt="" width="160" height="160" decoding="async"></button>
        <button type="button" class="thumb" aria-label="Softgels"><img src="{img}/hero-softgels.jpg?v={v}" alt="" width="160" height="160" loading="lazy" decoding="async"></button>
        <button type="button" class="thumb" aria-label="Ingredientes"><img src="{img}/hero-ingredients.jpg?v={v}" alt="" width="160" height="160" loading="lazy" decoding="async"></button>
        <button type="button" class="thumb" aria-label="Etiqueta"><img src="{img}/hero-label.jpg?v={v}" alt="" width="160" height="160" loading="lazy" decoding="async"></button>
        <button type="button" class="thumb" aria-label="MCT"><img src="{img}/hero-mct.jpg?v={v}" alt="" width="160" height="160" loading="lazy" decoding="async"></button>
      </div>
    </section>
"""
html = re.sub(
    r'<section class="gallery" id="heroSection">.*?</section>\s*\n\s*<section class="product-info">',
    gallery + "\n    <section class=\"product-info\">",
    html,
    count=1,
    flags=re.S,
)

product_info = """
      <div class="rating-row">
        <span class="stars">★★★★★</span>
        <a href="#resenas">4.9 Excelente · Información del producto</a>
      </div>

      <h1 class="product-title">Metabolae <em>Ceylon Cinnamon 7200 mg</em> — con MCT Oil · 300 Softgels</h1>

      <div class="price-row">
        <span class="price-now" id="priceNow">$39</span>
        <span class="price-was" id="priceWas">$59</span>
        <span class="price-save" id="priceSave">Ahorra 34%</span>
      </div>
      <p class="price-note">1 Bolsa · 300 softgels · Envío gratis · Pago al recibir</p>

      <ul class="hale-bullets">
        <li>Apoya tu rutina de bienestar metabólico con canela de Ceilán (<em>Cinnamomum verum</em>)</li>
        <li>Extracto concentrado equivalente a 7200 mg de canela cruda por softgel — confirma la porción en la etiqueta</li>
        <li>Aceite MCT como vehículo para ingredientes liposolubles</li>
        <li>300 softgels — presentación práctica para uso diario según indicaciones del fabricante</li>
      </ul>

      <div class="lab-badge">
        <i>✔</i>
        <div>
          <strong>Fórmula limpia · Sin gluten · Sin GMO · Sin soya</strong>
          <span>Suplemento alimenticio — no sustituye medicamentos ni consejo médico</span>
        </div>
      </div>

      <p class="live-count"><i></i><span id="liveViewing">48 personas viendo</span> | <span id="liveOrders">892 pedidos esta semana</span></p>

      <div class="buy-actions">
        <button type="button" class="btn-order js-open-order">Ordenar ahora — Pago al recibir</button>
        <p class="pay-note">No pagas nada ahora · Envío gratis a toda Panamá · Te confirmamos por WhatsApp</p>
      </div>

      <div class="hale-trust">
        <div>
          <img src="/images/nattokinase-hale/trust-guarantee.png?v=20260901d" alt="" width="56" height="56" loading="lazy" decoding="async">
          Garantía de 90 días
        </div>
        <div>
          <img src="/images/nattokinase-hale/trust-shipping.png?v=20260901d" alt="" width="56" height="56" loading="lazy" decoding="async">
          Envío gratis a toda Panamá
        </div>
        <div>
          <img src="/images/nattokinase-hale/trust-cgmp.png?v=20260901d" alt="" width="56" height="56" loading="lazy" decoding="async">
          Instalaciones certificadas
        </div>
      </div>

      <div class="trusted-by">
        <strong>Información clara antes de comprar</strong>
        revisa ingredientes, instrucciones y advertencias en la etiqueta del producto.
      </div>

      <div class="collapse-group">
        <div class="collapse">
          <button type="button" class="collapse-btn">Modo de uso <i>+</i></button>
          <div class="collapse-body">
            <p>Sigue las instrucciones del fabricante en el envase. No excedas la porción recomendada.</p>
            <p>Si tienes diabetes, tomas medicamentos, estás embarazada o en lactancia, consulta con un profesional de salud antes de utilizarlo.</p>
          </div>
        </div>
        <div class="collapse">
          <button type="button" class="collapse-btn">Beneficios <i>+</i></button>
          <div class="collapse-body">
            <ul>
              <li>La canela de Ceilán se ha estudiado por su posible relación con el metabolismo de la glucosa; los resultados pueden variar</li>
              <li>Variedad distinta de la canela cassia, generalmente con menos cumarina</li>
              <li>Complementa hábitos conscientes: alimentación equilibrada y actividad física</li>
              <li>Softgels fáciles de tragar — sin polvos ásperos</li>
            </ul>
          </div>
        </div>
        <div class="collapse">
          <button type="button" class="collapse-btn">Advertencias <i>+</i></button>
          <div class="collapse-body">
            <p>Este producto es un suplemento alimenticio. No está destinado a diagnosticar, tratar, curar o prevenir ninguna enfermedad.</p>
            <p>No modifiques tus medicamentos por tu cuenta. Mantén el producto fuera del alcance de los niños.</p>
          </div>
        </div>
      </div>
"""
html = re.sub(
    r'<section class="product-info">.*?</section>\s*\n\s*</div>\s*\n</main>',
    '<section class="product-info">' + product_info + "\n    </section>\n\n  </div>\n</main>",
    html,
    count=1,
    flags=re.S,
)

middle = f"""
<section class="voices" id="resenas">
  <div class="shell">
    <p class="hl-eyebrow">Apoya tu bienestar metabólico</p>
    <h2 class="hl-title">Canela de Ceilán para tu rutina diaria</h2>
    <p class="hl-lead">Incorpora Metabolae Ceylon Cinnamon a tu rutina de forma informada. Los resultados pueden variar y no están garantizados.</p>

    <div class="voices-track">
      <article class="voice">
        <img src="{img}/hero-product.jpg?v={v}" alt="" loading="lazy">
        <p class="voice-name">María L. · Panamá</p>
        <p>"Busqué canela de Ceilán específicamente, no cassia. La presentación en softgel me resulta práctica y la etiqueta lista MCT y extracto concentrado."</p>
        <cite>Opinión sobre el producto · presentación</cite>
      </article>
      <article class="voice">
        <img src="{img}/hero-softgels.jpg?v={v}" alt="" loading="lazy">
        <p class="voice-name">Carlos R. · Chitré</p>
        <p>"Me gusta que sean softgels y no cápsulas de polvo. Tomo uno al día según la etiqueta y acompaño con caminatas y mejor alimentación."</p>
        <cite>Opinión sobre uso y rutina</cite>
      </article>
      <article class="voice">
        <img src="{img}/hero-ingredients.jpg?v={v}" alt="" loading="lazy">
        <p class="voice-name">Ana P. · David</p>
        <p>"El paquete trae 300 unidades, así que dura bastante. Pago contra entrega en casa fue lo que me convenció para probarlo."</p>
        <cite>Opinión sobre pedido · envío</cite>
      </article>
    </div>
  </div>
</section>

<section class="hl-section hl-warm">
  <div class="shell">
    <div class="stats-layout">
      <div class="stats-panel">
        <h2>¿Estás cuidando tu salud metabólica?</h2>
        <p>Entre el trabajo y una rutina acelerada, mantener hábitos saludables no siempre es fácil: alimentación poco equilibrada, poca actividad física y poco tiempo para cuidarte.</p>
        <b>Empieza a prestar más atención a tu bienestar — con información clara.</b>
      </div>
      <div class="stat-bars">
        <div class="stat-bar">
          <img src="{img}/hero-label.jpg?v={v}" alt="" loading="lazy">
          <strong>7200 mg</strong>
          <span>Equivalente declarado por softgel — verifica en la etiqueta</span>
        </div>
        <div class="stat-bar">
          <img src="{img}/hero-mct.jpg?v={v}" alt="" loading="lazy">
          <strong>MCT</strong>
          <span>Aceite de cadena media como vehículo liposoluble</span>
        </div>
        <div class="stat-bar">
          <img src="{img}/hero-softgels.jpg?v={v}" alt="" loading="lazy">
          <strong>300</strong>
          <span>Softgels por bolsa</span>
        </div>
        <div class="stat-bar">
          <img src="{img}/hero-ingredients.jpg?v={v}" alt="" loading="lazy">
          <strong>Ceilán</strong>
          <span><em>Cinnamomum verum</em> — no cassia</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="hl-section hl-warm" style="padding-top:0">
  <div class="shell">
    <div class="mech-head">
      <h2>Descubre los beneficios de la canela de Ceilán</h2>
      <p>Información educativa. Este suplemento no sustituye medicamentos, tratamientos médicos ni una alimentación equilibrada.</p>
    </div>
    <div class="mech-track" id="mechTrack">
      <button type="button" class="mech-card is-active">
        <img src="{img}/hero-product.jpg?v={v}" alt="" loading="lazy">
        <h3>Apoyo metabólico</h3>
        <p>La canela ha sido estudiada por su posible relación con el metabolismo de la glucosa. Los resultados pueden variar y no están garantizados.</p>
      </button>
      <button type="button" class="mech-card">
        <img src="{img}/hero-softgels.jpg?v={v}" alt="" loading="lazy">
        <h3>Sensibilidad a la insulina</h3>
        <p>La sensibilidad a la insulina es un aspecto importante de la salud metabólica. La canela se investiga por su posible papel en este proceso.</p>
      </button>
      <button type="button" class="mech-card">
        <img src="{img}/hero-ingredients.jpg?v={v}" alt="" loading="lazy">
        <h3>Salud metabólica</h3>
        <p>Complementa tu rutina con decisiones conscientes, alimentación equilibrada y actividad física regular.</p>
      </button>
      <button type="button" class="mech-card">
        <img src="{img}/hero-label.jpg?v={v}" alt="" loading="lazy">
        <h3>Canela de Ceilán</h3>
        <p>Variedad distinta de la canela cassia; generalmente contiene menos cumarina.</p>
      </button>
      <button type="button" class="mech-card">
        <img src="{img}/hero-mct.jpg?v={v}" alt="" loading="lazy">
        <h3>Presentación concentrada</h3>
        <p>Forma práctica de incorporar este ingrediente botánico. Consulta la etiqueta para confirmar la cantidad por porción.</p>
      </button>
      <button type="button" class="mech-card">
        <img src="{img}/hero-product.jpg?v={v}" alt="" loading="lazy">
        <h3>Fácil de incorporar</h3>
        <p>Sigue las instrucciones del fabricante y acompaña tu rutina con hábitos saludables.</p>
      </button>
    </div>
  </div>
</section>

<section class="hl-section hl-cream ingc-section">
  <div class="ingc">
    <div class="ingc__header">
      <h2 class="ingc__heading">Conoce su ingrediente principal</h2>
      <p class="ingc__sub">Canela de Ceilán · MCT Oil · Softgels</p>
    </div>
    <div class="ingc__wrap">
      <button type="button" class="ingc__arr ingc__arr--l" aria-label="Ingrediente anterior">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M12 3L6 9L12 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
      </button>
      <div class="ingc__track">
        <button type="button" class="ingc__card is-flipped" data-idx="0">
          <span class="ingc__card-inner">
            <span class="ingc__card-front">
              <img src="{img}/hero-ingredients.jpg?v={v}" alt="" class="ingc__card-img" loading="lazy">
              <span class="ingc__card-label"><span>Canela de Ceilán</span></span>
            </span>
            <span class="ingc__card-back">
              <span class="ingc__card-title">Cinnamomum verum</span>
              <span class="ingc__card-dose">7200 mg equivalente*</span>
              <span class="ingc__card-desc">Especia de origen vegetal utilizada tradicionalmente. Verifica en la etiqueta qué significa exactamente la cifra de 7200 mg por porción.</span>
            </span>
          </span>
        </button>
        <button type="button" class="ingc__card" data-idx="1">
          <span class="ingc__card-inner">
            <span class="ingc__card-front">
              <img src="{img}/hero-mct.jpg?v={v}" alt="" class="ingc__card-img" loading="lazy">
              <span class="ingc__card-label"><span>Aceite MCT</span></span>
            </span>
            <span class="ingc__card-back">
              <span class="ingc__card-title">MCT Oil</span>
              <span class="ingc__card-dose">Vehículo liposoluble</span>
              <span class="ingc__card-desc">Triglicéridos de cadena media como soporte de absorción para compuestos liposolubles de la canela.</span>
            </span>
          </span>
        </button>
        <button type="button" class="ingc__card" data-idx="2">
          <span class="ingc__card-inner">
            <span class="ingc__card-front">
              <img src="{img}/hero-softgels.jpg?v={v}" alt="" class="ingc__card-img" loading="lazy">
              <span class="ingc__card-label"><span>Softgels</span></span>
            </span>
            <span class="ingc__card-back">
              <span class="ingc__card-title">Softgel</span>
              <span class="ingc__card-dose">300 por bolsa</span>
              <span class="ingc__card-desc">Presentación blanda pensada para uso diario según las instrucciones del fabricante.</span>
            </span>
          </span>
        </button>
      </div>
      <button type="button" class="ingc__arr ingc__arr--r" aria-label="Ingrediente siguiente">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M6 3L12 9L6 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
      </button>
    </div>
  </div>
</section>

<section class="hl-section hl-beige">
  <div class="shell">
    <p class="hl-eyebrow">¿Cómo incorporarlo?</p>
    <h2 class="hl-title">Metabolae en tu rutina diaria</h2>
    <div class="tl" id="cinnamon-timeline">
      <div class="tl-step tl-step--left">
        <div class="tl-card">
          <h3>1. Revisa la etiqueta</h3>
          <ul>
            <li>Consulta ingredientes e instrucciones del fabricante.</li>
            <li>Confirma alérgenos y advertencias.</li>
          </ul>
        </div>
        <span class="tl-marker" aria-hidden="true"><svg class="tl-check" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10 17.5L19 7.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
      </div>
      <div class="tl-step tl-step--right">
        <div class="tl-card">
          <h3>2. Sigue la porción indicada</h3>
          <ul>
            <li>No excedas la cantidad recomendada en el envase.</li>
            <li>Consulta a tu médico si tomas medicamentos para la glucosa.</li>
          </ul>
        </div>
        <span class="tl-marker" aria-hidden="true"><svg class="tl-check" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10 17.5L19 7.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
      </div>
      <div class="tl-step tl-step--left">
        <div class="tl-card">
          <h3>3. Mantén hábitos saludables</h3>
          <ul>
            <li>Alimentación equilibrada, actividad física y descanso.</li>
            <li>Este suplemento no reemplaza tratamientos prescritos.</li>
          </ul>
        </div>
        <span class="tl-marker" aria-hidden="true"><svg class="tl-check" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10 17.5L19 7.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
      </div>
    </div>
  </div>
</section>

<section class="hl-section hl-cream">
  <div class="shell">
    <p class="hl-eyebrow">Preguntas frecuentes</p>
    <h2 class="hl-title">Todo lo que debes saber</h2>
    <div class="faq-list" id="faqList">
      <div class="faq-item"><button type="button" class="faq-q">¿Qué es Metabolae Ceylon Cinnamon 7200 mg? <i>+</i></button><div class="faq-a">Es un suplemento a base de canela de Ceilán. Consulta la etiqueta para la composición completa y la cantidad por porción.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Ayuda a mantener niveles saludables de azúcar en la sangre? <i>+</i></button><div class="faq-a">La canela ha sido estudiada por su posible relación con el metabolismo de la glucosa, pero no se pueden garantizar resultados específicos.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Qué diferencia hay entre canela de Ceilán y cassia? <i>+</i></button><div class="faq-a">Son variedades distintas. La canela de Ceilán generalmente contiene menos cumarina que la cassia.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Cómo debo tomarlo? <i>+</i></button><div class="faq-a">Sigue las instrucciones y la porción indicada en el envase. No excedas la cantidad recomendada.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Puedo tomarlo si tengo diabetes? <i>+</i></button><div class="faq-a">Consulta con tu médico antes de utilizarlo, especialmente si tomas medicamentos para controlar la glucosa. No reemplaza ningún tratamiento prescrito.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Realizan envíos en Panamá? <i>+</i></button><div class="faq-a">Sí — envío gratis a toda Panamá con pago contra entrega en la mayoría de zonas.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Puedo pagar contra entrega? <i>+</i></button><div class="faq-a">Sí. No pagas por adelantado: pagas en efectivo cuando recibes tu pedido en casa.</div></div>
      <div class="faq-item"><button type="button" class="faq-q">¿Y si no me convence? <i>+</i></button><div class="faq-a">Garantía de 90 días. Escríbenos dentro del plazo indicado en nuestra política de devoluciones.</div></div>
    </div>
  </div>
</section>

<section class="hl-section hl-warm safety">
  <div class="shell safety-inner">
    <h2>Haz de tu bienestar una prioridad</h2>
    <p class="safety-lead">Incorpora Metabolae Ceylon Cinnamon de forma informada. Completa tus datos y confirma precio, dirección y pago contra entrega.</p>
    <button type="button" class="btn-order js-open-order">¡Haz tu pedido ahora!</button>
  </div>
</section>
"""

html = re.sub(
    r'<section class="voices" id="resenas">.*?<footer class="site-footer">',
    middle + '\n<footer class="site-footer">',
    html,
    count=1,
    flags=re.S,
)

# Remove review lightbox block if still present
html = re.sub(r'<div class="review-lightbox".*?</div>\s*\n', "", html, count=1, flags=re.S)

# Sticky + modal
html = html.replace('id="stickyPrice">$42', 'id="stickyPrice">$39')
html = html.replace('id="stickyLabel">1 Frasco · 80 días', 'id="stickyLabel">1 Bolsa · 300 softgels')
html = html.replace(
    'src="/images/nattokinase-hale/hero-bottle-clinical.jpg?v=20260831r"',
    f'src="{img}/hero-product.jpg?v={v}"',
)
html = html.replace("<strong>Nattokinasa 10,000 FU</strong>", "<strong>Metabolae Ceylon Cinnamon</strong>")
html = html.replace("<span>240 cápsulas · Envío gratis</span>", "<span>300 softgels · Envío gratis</span>")
html = html.replace('name="source" value="nattokinase-panama"', 'name="source" value="metabolae-ceylon-cinnamon-panama"')
html = html.replace('id="orderTotal" value="42"', 'id="orderTotal" value="39"')

bundles_old = re.search(r'<span class="block-label">1\. Elige tu oferta</span>.*?</div>\s*\n\s*<div class="form-head">', html, re.S)
if bundles_old:
    bundles_new = """<span class="block-label">1. Elige tu oferta</span>
        <div class="bundles">
          <label class="bundle bundle-option is-selected">
            <input type="radio" name="bundleOption" value="cc-cinnamon-pa-1" data-product-id="cc-cinnamon-pa-1" data-product-name="Metabolae Ceylon Cinnamon - 1 bolsa" data-price="39" data-old-price="59" data-save="34" data-label="1 Bolsa · 300 softgels" checked>
            <div class="bundle-card">
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>1 Bolsa</span>
                <span class="bundle-cost"><strong>$39</strong><del>$59</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot green"></span>300 softgels · uso según etiqueta</span>
              </div>
            </div>
          </label>
          <label class="bundle bundle-option">
            <input type="radio" name="bundleOption" value="cc-cinnamon-pa-2" data-product-id="cc-cinnamon-pa-2" data-product-name="Metabolae Ceylon Cinnamon - 2 bolsas" data-price="59" data-old-price="88" data-save="33" data-label="2 Bolsas · 600 softgels">
            <div class="bundle-card">
              <span class="bundle-flag">Más popular</span>
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>2 Bolsas</span>
                <span class="bundle-cost"><strong>$59</strong><del>$88</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot green"></span>600 softgels · Ahorra $19</span>
              </div>
            </div>
          </label>
          <label class="bundle bundle-option">
            <input type="radio" name="bundleOption" value="cc-cinnamon-pa-3" data-product-id="cc-cinnamon-pa-3" data-product-name="Metabolae Ceylon Cinnamon - 3 bolsas" data-price="79" data-old-price="117" data-save="32" data-label="3 Bolsas · 900 softgels">
            <div class="bundle-card">
              <span class="bundle-flag">Mejor valor</span>
              <div class="bundle-head">
                <span class="bundle-pick"><span class="radio"></span>3 Bolsas</span>
                <span class="bundle-cost"><strong>$79</strong><del>$117</del></span>
              </div>
              <div class="bundle-units">
                <span class="unit-chip"><span class="dot green"></span>900 softgels · Ahorra $38</span>
              </div>
            </div>
          </label>
        </div>

        <div class="form-head">"""
    html = html.replace(bundles_old.group(0), bundles_new, 1)

html = html.replace('id="sumSubtotal">$42', 'id="sumSubtotal">$39')
html = html.replace('id="sumTotal">$42', 'id="sumTotal">$39')
html = html.replace("getElementById('natto-timeline')", "getElementById('cinnamon-timeline')")

# Drop review lightbox JS block
html = re.sub(
    r"\n  var lightbox = document\.getElementById\('reviewLightbox'\);.*?  \}\n\n  var viewing",
    "\n  var viewing",
    html,
    count=1,
    flags=re.S,
)

html = html.replace("centerCard(2);", "centerCard(1);")

path.write_text(html, encoding="utf-8")
print("Patched", path, "length", len(html))
