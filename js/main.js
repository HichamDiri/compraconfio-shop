// فخر الخليج — minimal JS for speed
(function() {
  function bootstrapFacebookPixel() {
    (function(f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function() {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = true;
      n.version = '2.0';
      n.queue = [];
      t = b.createElement(e);
      t.async = true;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
  }

  var earlyFbPixelId = document.body && document.body.dataset.fbPixelId
    ? document.body.dataset.fbPixelId
    : '';
  if (earlyFbPixelId && !window.fbq) {
    bootstrapFacebookPixel();
    window.fbq('init', earlyFbPixelId);
    window.fbq('track', 'PageView');
  }
})();

document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('orderForm');
  var bottomSticky = document.getElementById('bottomSticky');
  var heroSection = document.getElementById('heroSection');
  var checkoutSection = document.getElementById('checkout');
  var nameInput = document.getElementById('name');

  function runWhenIdle(callback) {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(callback, { timeout: 3500 });
      return;
    }

    setTimeout(callback, 2500);
  }

  function loadScript(src) {
    var script = document.createElement('script');
    script.async = true;
    script.src = src;
    document.head.appendChild(script);
    return script;
  }

  function initFacebookPixel(pixelId) {
    if (!pixelId) return;

    if (!window.fbq) {
      (function(f, b, e, v, n, t, s) {
        if (f.fbq) return;
        n = f.fbq = function() {
          n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
        };
        if (!f._fbq) f._fbq = n;
        n.push = n;
        n.loaded = true;
        n.version = '2.0';
        n.queue = [];
        t = b.createElement(e);
        t.async = true;
        t.src = v;
        s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t, s);
      })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    }

    window.fbq('init', pixelId);
    window.fbq('track', 'PageView');
  }

  function initTikTokPixel(pixelId) {
    if (!pixelId) return;

    if (!window.ttq) {
      !function(w, d, t) {
        w.TiktokAnalyticsObject = t;
        var ttq = w[t] = w[t] || [];
        ttq.methods = ['page', 'track', 'identify', 'instances', 'debug', 'on', 'off', 'once', 'ready', 'alias', 'group', 'enableCookie', 'disableCookie', 'holdConsent', 'revokeConsent', 'grantConsent'];
        ttq.setAndDefer = function(target, method) {
          target[method] = function() {
            target.push([method].concat(Array.prototype.slice.call(arguments, 0)));
          };
        };
        for (var i = 0; i < ttq.methods.length; i++) {
          ttq.setAndDefer(ttq, ttq.methods[i]);
        }
        ttq.load = function(id, options) {
          var src = 'https://analytics.tiktok.com/i18n/pixel/events.js';
          ttq._i = ttq._i || {};
          ttq._i[id] = [];
          ttq._i[id]._u = src;
          ttq._t = ttq._t || {};
          ttq._t[id] = +new Date();
          ttq._o = ttq._o || {};
          ttq._o[id] = options || {};
          var script = d.createElement('script');
          script.type = 'text/javascript';
          script.async = true;
          script.src = src + '?sdkid=' + id + '&lib=' + t;
          var firstScript = d.getElementsByTagName('script')[0];
          firstScript.parentNode.insertBefore(script, firstScript);
        };
      }(window, document, 'ttq');
    }

    if (!window.__tiktokPixelLoaded) {
      window.ttq.load(pixelId);
      window.ttq.page();
      window.__tiktokPixelLoaded = true;
    }
  }

  function trackTikTok(eventName, params) {
    if (!window.ttq || typeof window.ttq.track !== 'function') return;
    window.ttq.track(eventName, params || {});
  }

  function getTikTokPixelId() {
    return document.body && document.body.dataset.tiktokPixelId
      ? document.body.dataset.tiktokPixelId
      : '';
  }

  function getTrackingSnapshot(formEl) {
    var trackingForm = formEl || document.getElementById('orderForm');
    var trackingData = trackingForm ? new FormData(trackingForm) : null;
    var selectedBundle = trackingForm ? trackingForm.querySelector('input[name="bundleOption"]:checked') : null;
    return {
      productId: selectedBundle
        ? String(selectedBundle.dataset.productId || selectedBundle.value || '').trim()
        : String(trackingData ? trackingData.get('productId') || '' : '').trim(),
      price: selectedBundle
        ? Number(selectedBundle.dataset.price || 0)
        : Number(trackingData ? trackingData.get('price') || 0 : 0),
      currency: String(trackingData ? trackingData.get('currency') || 'GTQ' : 'GTQ').trim(),
      contentName: selectedBundle
        ? String(selectedBundle.dataset.productName || '').trim()
        : String(trackingData ? trackingData.get('productName') || '' : '').trim()
    };
  }

  function getFbPixelId() {
    return document.body && document.body.dataset.fbPixelId
      ? document.body.dataset.fbPixelId
      : '';
  }

  function getInitiateCheckoutDedupeKey() {
    var product = document.body && document.body.dataset.product
      ? document.body.dataset.product
      : window.location.pathname;
    return 'fb_initiate_checkout_' + product;
  }

  function trackFacebookInitiateCheckout() {
    var fbPixelId = getFbPixelId();
    if (!fbPixelId) return;

    var dedupeKey = getInitiateCheckoutDedupeKey();
    if (sessionStorage.getItem(dedupeKey)) return;

    if (!window.fbq) {
      initFacebookPixel(fbPixelId);
    }
    if (!window.fbq) return;

    var snapshot = getTrackingSnapshot();
    var productId = snapshot.productId;
    var price = snapshot.price || 0;
    var currency = snapshot.currency || 'GTQ';
    var contentName = snapshot.contentName;
    var trackingForm = document.getElementById('orderForm');
    var totalEl = trackingForm
      ? (trackingForm.querySelector('#orderTotal') || trackingForm.querySelector('[name="total"]'))
      : null;
    var checkoutValue = totalEl ? Number(totalEl.value || 0) : price;
    if (!checkoutValue) checkoutValue = price;

    if (!checkoutValue && !productId) return;

    window.fbq('track', 'InitiateCheckout', {
      content_ids: productId ? [productId] : [],
      content_name: contentName,
      content_type: 'product',
      value: checkoutValue,
      currency: currency,
      num_items: 1
    });

    sessionStorage.setItem(dedupeKey, '1');
  }

  function getTikTokInitiateCheckoutDedupeKey() {
    var product = document.body && document.body.dataset.product
      ? document.body.dataset.product
      : window.location.pathname;
    return 'tt_initiate_checkout_' + product;
  }

  function trackTikTokInitiateCheckout() {
    var tiktokPixelId = getTikTokPixelId();
    if (!tiktokPixelId) return;

    var dedupeKey = getTikTokInitiateCheckoutDedupeKey();
    if (sessionStorage.getItem(dedupeKey)) return;

    initTikTokPixel(tiktokPixelId);

    var snapshot = getTrackingSnapshot();
    var productId = snapshot.productId;
    var price = snapshot.price || 0;
    var currency = snapshot.currency || 'GTQ';
    var contentName = snapshot.contentName;
    var trackingForm = document.getElementById('orderForm');
    var totalEl = trackingForm
      ? (trackingForm.querySelector('#orderTotal') || trackingForm.querySelector('[name="total"]'))
      : null;
    var checkoutValue = totalEl ? Number(totalEl.value || 0) : price;
    if (!checkoutValue) checkoutValue = price;

    if (!checkoutValue && !productId) return;

    trackTikTok('InitiateCheckout', {
      content_id: productId,
      content_type: 'product',
      content_name: contentName,
      value: checkoutValue,
      currency: currency
    });

    sessionStorage.setItem(dedupeKey, '1');
  }

  function loadTracking() {
    (function(c, a) {
      c[a] = c[a] || function() {
        (c[a].q = c[a].q || []).push(arguments);
      };
    })(window, 'clarity');
    loadScript('https://www.clarity.ms/tag/j40qeluzew');

    var fbPixelId = document.body && document.body.dataset.fbPixelId
      ? document.body.dataset.fbPixelId
      : '';
    var snapshot = getTrackingSnapshot();
    var trackingProductId = snapshot.productId || 'cc-mascara-1';
    var trackingPrice = snapshot.price || 299;
    var trackingCurrency = snapshot.currency || 'GTQ';

    if (fbPixelId) {
      if (!window.fbq) {
        initFacebookPixel(fbPixelId);
      }
      if (window.fbq) {
        window.fbq('track', 'ViewContent', {
          content_ids: [trackingProductId],
          content_type: 'product',
          value: trackingPrice,
          currency: trackingCurrency
        });
      }
    }

    var tiktokPixelId = getTikTokPixelId();
    if (tiktokPixelId) {
      initTikTokPixel(tiktokPixelId);
      trackTikTok('ViewContent', {
        content_id: trackingProductId,
        content_type: 'product',
        content_name: snapshot.contentName || '',
        value: trackingPrice,
        currency: trackingCurrency
      });
    }

    if (document.body && document.body.dataset.snapPixel !== 'off') {
      var snapPixelId = document.body && document.body.dataset.snapPixelId
        ? document.body.dataset.snapPixelId
        : '628aaf3b-352d-439a-b974-be09e95eb972';

      (function(e) {
        if (e.snaptr) return;
        var a = e.snaptr = function() {
          a.handleRequest ? a.handleRequest.apply(a, arguments) : a.queue.push(arguments);
        };
        a.queue = [];
      })(window);
      loadScript('https://sc-static.net/scevent.min.js');

      window.snaptr('init', snapPixelId, {});
      window.snaptr('track', 'PAGE_VIEW');
      window.snaptr('track', 'VIEW_CONTENT', {
        item_ids: [trackingProductId],
        item_category: 'beauty',
        price: trackingPrice,
        currency: trackingCurrency
      });
    }
  }

  window.addEventListener('load', function() {
    runWhenIdle(loadTracking);
  }, { once: true });

  if (checkoutSection) {
    document.querySelectorAll('a[href="#checkout"]').forEach(function(link) {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        if (bottomSticky && link.closest('#bottomSticky')) {
          bottomSticky.classList.remove('is-visible');
          bottomSticky.setAttribute('aria-hidden', 'true');
        }
        checkoutSection.scrollIntoView({ behavior: 'auto', block: 'start' });
        window.history.replaceState(null, '', '#checkout');
        if (nameInput) nameInput.focus({ preventScroll: true });
      });
    });
  }

  if (bottomSticky && heroSection) {
    var stickyMode = document.body && document.body.dataset.stickyMode;
    var toggleSticky = function() {
      var showSticky;
      if (stickyMode === 'content' && checkoutSection) {
        showSticky = checkoutSection.getBoundingClientRect().bottom <= 0;
      } else {
        var heroRect = heroSection.getBoundingClientRect();
        var heroHalfPassed = heroRect.top + heroRect.height * 0.5 <= 0;
        var checkoutTop = checkoutSection ? checkoutSection.getBoundingClientRect().top : Infinity;
        showSticky = heroHalfPassed && checkoutTop > window.innerHeight;
      }
      bottomSticky.classList.toggle('is-visible', showSticky);
      bottomSticky.setAttribute('aria-hidden', showSticky ? 'false' : 'true');
    };

    toggleSticky();
    window.addEventListener('scroll', toggleSticky, { passive: true });
    window.addEventListener('resize', toggleSticky);
  }

  if (!form) return;

  function getSelectedBundle() {
    return form.querySelector('input[name="bundleOption"]:checked');
  }

  function getProductSelection(formData) {
    var selectedBundle = getSelectedBundle();

    if (selectedBundle) {
      return {
        productId: String(selectedBundle.dataset.productId || selectedBundle.value || '').trim(),
        productName: String(selectedBundle.dataset.productName || 'كوزما كولاجين').trim(),
        price: String(selectedBundle.dataset.price || '199').trim(),
        oldPrice: String(selectedBundle.dataset.oldPrice || '').trim(),
        currency: String(formData.get('currency') || 'SAR').trim()
      };
    }

    return {
      productId: String(formData.get('productId') || 'anti-cellulite-massager').trim(),
      productName: String(formData.get('productName') || 'جهاز تدليك لإزالة السيلوليت').trim(),
      price: String(formData.get('price') || '199').trim(),
      oldPrice: '',
      currency: String(formData.get('currency') || 'SAR').trim()
    };
  }

  function getCurrencyLabels(currency) {
    if (currency === 'GTQ') {
      return { full: 'quetzales', short: 'Q' };
    }

    if (currency === 'QAR') {
      return { full: 'ريال قطري', short: 'ر.ق' };
    }

    if (currency === 'AED') {
      return { full: 'درهم', short: 'د.إ' };
    }

    if (currency === 'BHD') {
      return { full: 'دينار بحريني', short: 'د.ب' };
    }

    if (currency === 'SAR') {
      return { full: 'ريال سعودي', short: 'ر.س' };
    }

    return { full: currency, short: currency };
  }

  function isSpanishPage() {
    return document.body && document.body.dataset.lang === 'es';
  }

  function formatPrice(value, currency) {
    var labels = getCurrencyLabels(currency);
    if (currency === 'GTQ') {
      return labels.short + value + ' ' + labels.full;
    }
    return value + ' ' + labels.full;
  }

  function formatShortPrice(value, currency) {
    var labels = getCurrencyLabels(currency);
    if (currency === 'GTQ') {
      return labels.short + value;
    }
    return value + ' ' + labels.short;
  }

  function syncBundlePrice() {
    var formData = new FormData(form);
    var selection = getProductSelection(formData);
    var selectedBundle = getSelectedBundle();
    var shortPrice = formatShortPrice(selection.price, selection.currency);

    form.querySelectorAll('.bundle-option').forEach(function(label) {
      var input = label.querySelector('input[name="bundleOption"]');
      label.classList.toggle('is-selected', Boolean(input && input.checked));
    });

    document.querySelectorAll('[data-selected-price]').forEach(function(element) {
      var stickyFromPrice = element.getAttribute('data-sticky-from-price');
      if (stickyFromPrice) {
        element.textContent = formatShortPrice(stickyFromPrice, selection.currency);
        return;
      }
      element.textContent = element.closest('#bottomSticky') ? shortPrice : formatPrice(selection.price, selection.currency);
    });

    document.querySelectorAll('[data-selected-old-price]').forEach(function(element) {
      element.textContent = selection.oldPrice ? formatPrice(selection.oldPrice, selection.currency) : '';
    });

    if (selectedBundle) {
      document.querySelectorAll('[data-selected-offer]').forEach(function(element) {
        element.textContent = String(selectedBundle.dataset.stickyOffer || selectedBundle.dataset.productName || '').trim();
      });
    }
  }

  form.querySelectorAll('input[name="bundleOption"]').forEach(function(option) {
    option.addEventListener('change', syncBundlePrice);
  });
  syncBundlePrice();

  function normalizeSaudiPhone(value) {
    var digits = String(value || '').replace(/[^\d]/g, '');

    if (/^05[0-9]{8}$/.test(digits)) {
      return digits;
    }

    if (/^9665[0-9]{8}$/.test(digits)) {
      return '0' + digits.slice(3);
    }

    if (/^5[0-9]{8}$/.test(digits)) {
      return '0' + digits;
    }

    return '';
  }

  function normalizeQatarPhone(value) {
    var digits = String(value || '').replace(/[^\d]/g, '');

    if (/^[3567][0-9]{7}$/.test(digits)) {
      return digits;
    }

    if (/^974[3567][0-9]{7}$/.test(digits)) {
      return digits.slice(3);
    }

    return '';
  }

  function normalizeUaePhone(value) {
    var digits = String(value || '').replace(/[^\d]/g, '');

    if (/^05[0-9]{8}$/.test(digits)) {
      return digits;
    }

    if (/^9715[0-9]{8}$/.test(digits)) {
      return '0' + digits.slice(3);
    }

    if (/^5[0-9]{8}$/.test(digits)) {
      return '0' + digits;
    }

    return '';
  }

  function normalizeBahrainPhone(value) {
    var digits = String(value || '').replace(/[^\d]/g, '');

    if (/^0[36][0-9]{7}$/.test(digits)) {
      return digits.slice(1);
    }

    if (/^[36][0-9]{7}$/.test(digits)) {
      return digits;
    }

    if (/^973[36][0-9]{7}$/.test(digits)) {
      return digits.slice(3);
    }

    return '';
  }

  function normalizeGuatemalaPhone(value) {
    var digits = String(value || '').replace(/[^\d]/g, '');

    if (/^502[34567][0-9]{7}$/.test(digits)) {
      return digits.slice(3);
    }

    if (/^[34567][0-9]{7}$/.test(digits)) {
      return digits;
    }

    return '';
  }

  function normalizeLenientPhone(value) {
    var digits = String(value || '').replace(/[^\d]/g, '');
    return digits.length >= 7 && digits.length <= 15 ? digits : '';
  }

  function normalizePhone(value, country) {
    if (country === 'GT') {
      return normalizeGuatemalaPhone(value);
    }

    if (country === 'QA') {
      return normalizeQatarPhone(value);
    }

    if (country === 'AE') {
      return normalizeUaePhone(value);
    }

    if (country === 'BH') {
      return normalizeBahrainPhone(value);
    }

    return normalizeSaudiPhone(value);
  }

  function createOrderId() {
    if (document.body && document.body.dataset.brand === 'compraconfio') {
      return 'CC-' + Date.now().toString().slice(-8);
    }
    if (document.body && document.body.dataset.country === 'GT') {
      return 'LGT-' + Date.now().toString().slice(-8);
    }
    return 'FK-' + Date.now().toString().slice(-8);
  }

  function getThankYouPath() {
    return document.body && document.body.dataset.thankyou
      ? document.body.dataset.thankyou
      : '/thank-you.html';
  }

  function goToThankYou(payload, orderId) {
    var params = new URLSearchParams();
    Object.keys(payload).forEach(function(key) {
      if (payload[key] != null && payload[key] !== '') {
        params.set(key, String(payload[key]));
      }
    });
    params.set('order', orderId);
    var fbPixelId = document.body && document.body.dataset.fbPixelId
      ? document.body.dataset.fbPixelId
      : '';
    if (fbPixelId) {
      params.set('fbPixelId', fbPixelId);
    }
    var tiktokPixelId = document.body && document.body.dataset.tiktokPixelId
      ? document.body.dataset.tiktokPixelId
      : '';
    if (tiktokPixelId) {
      params.set('tiktokPixelId', tiktokPixelId);
    }
    window.location.href = getThankYouPath() + '?' + params.toString();
  }

  function hasOrderEndpoint() {
    return Boolean(window.GOOGLE_SHEETS_URL || window.ORDER_API_URL);
  }

  function submitToGoogleSheets(url, payload) {
    var body = new URLSearchParams();
    body.append('payload', JSON.stringify(payload));

    if (typeof navigator.sendBeacon === 'function' && navigator.sendBeacon(url, body)) {
      return Promise.resolve({ ok: true, order: { id: payload.orderId } });
    }

    return fetch(url, {
      method: 'POST',
      mode: 'no-cors',
      keepalive: true,
      body: body
    }).then(function() {
      return { ok: true, order: { id: payload.orderId } };
    });
  }

  function submitOrder(payload) {
    if (window.GOOGLE_SHEETS_URL) {
      return submitToGoogleSheets(window.GOOGLE_SHEETS_URL, payload);
    }

    return fetch(window.ORDER_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      keepalive: true,
      body: JSON.stringify(payload)
    }).then(function(response) {
      return response.json();
    });
  }

  form.addEventListener('submit', async function(e) {
    var phone = document.getElementById('phone');
    var submitButton = form.querySelector('button[type="submit"]');
    var formDataForCountry = new FormData(form);
    var country = document.body && document.body.dataset.country
      ? document.body.dataset.country
      : (formDataForCountry.get('currency') === 'GTQ'
        ? 'GT'
        : (formDataForCountry.get('currency') === 'QAR'
        ? 'QA'
        : (formDataForCountry.get('currency') === 'AED'
          ? 'AE'
          : (formDataForCountry.get('currency') === 'BHD' ? 'BH' : 'SA'))));
    var phoneLenient = document.body && document.body.dataset.phoneLenient === 'on';
    var normalizedPhone = phoneLenient
      ? normalizeLenientPhone(phone.value)
      : normalizePhone(phone.value, country);

    if (!normalizedPhone) {
      e.preventDefault();
      if (isSpanishPage()) {
        alert(phoneLenient
          ? 'Por favor ingresa un número de teléfono válido'
          : (country === 'GT'
            ? 'Por favor ingresa un número guatemalteco válido (ej: 55123456 o +50255123456)'
            : 'Por favor ingresa un número de teléfono válido'));
      } else {
        alert(phoneLenient
          ? 'يرجى إدخال رقم هاتف صحيح'
          : (country === 'QA'
          ? 'يرجى إدخال رقم هاتف قطري صحيح (مثال: 55123456 أو +97455123456)'
          : (country === 'AE'
            ? 'يرجى إدخال رقم هاتف إماراتي صحيح (مثال: 0501234567 أو +971501234567)'
            : (country === 'BH'
              ? 'يرجى إدخال رقم هاتف بحريني صحيح (مثال: 39123456 أو 039123456 أو +97339123456)'
              : 'يرجى إدخال رقم جوال سعودي صحيح (مثال: 0541962123 أو +966541962123)'))));
      }
      phone.focus();
      return;
    }

    phone.value = normalizedPhone;
    trackFacebookInitiateCheckout();
    trackTikTokInitiateCheckout();

    if (!hasOrderEndpoint()) {
      return;
    }

    e.preventDefault();

    var formData = new FormData(form);
    var selection = getProductSelection(formData);
    var selectedBundle = getSelectedBundle();
    var addressValue = String(formData.get('address') || '').trim();
    var addressLineValue = String(formData.get('addressLine') || '').trim();
    var zoneValue = String(formData.get('zone') || '').trim();
    var departmentValue = String(formData.get('department') || '').trim();
    var cityValue = String(formData.get('city') || '').trim();
    var countryValue = String(formData.get('country') || '').trim();
    var firstNameValue = String(formData.get('firstName') || '').trim();
    var lastNameValue = String(formData.get('lastName') || '').trim();
    var nameValue = String(formData.get('name') || '').trim();
    if (!nameValue && (firstNameValue || lastNameValue)) {
      nameValue = (firstNameValue + ' ' + lastNameValue).trim();
    }
    if (cityValue) {
      addressValue = cityValue + (addressValue ? ', ' + addressValue : '');
    }
    if (departmentValue) {
      addressValue = addressValue ? addressValue + ', ' + departmentValue : departmentValue;
    }
    if (countryValue) {
      addressValue = addressValue ? addressValue + ', ' + countryValue : countryValue;
    }
    var payload = {
      orderId: createOrderId(),
      productId: selection.productId,
      productName: selection.productName,
      price: selection.price,
      currency: selection.currency,
      name: nameValue,
      firstName: firstNameValue,
      lastName: lastNameValue,
      phone: normalizedPhone,
      address: addressValue,
      addressLine: addressLineValue,
      zone: zoneValue,
      city: cityValue,
      country: countryValue,
      department: departmentValue,
      bundleLabel: selectedBundle ? String(selectedBundle.dataset.label || '').trim() : '',
      color: String(formData.get('color') || '').trim(),
      createdAt: new Date().toISOString(),
      source: String(formData.get('source') || 'compraconfio').trim()
    };

    var shippingMethodValue = String(formData.get('shippingMethod') || '').trim();
    if (shippingMethodValue) {
      payload.shippingMethod = shippingMethodValue;
      payload.shipping = String(formData.get('shipping') || '0').trim();
      payload.total = String(formData.get('total') || selection.price).trim();
    }

    try {
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = isSpanishPage() ? 'Confirmando pedido...' : 'جاري تأكيد الطلب...';
      }

      var result = await submitOrder(payload);
      if (!result || !result.ok) {
        throw new Error(result.message || (isSpanishPage() ? 'No se pudo enviar el pedido' : 'تعذر إرسال الطلب'));
      }

      goToThankYou(payload, result.order && result.order.id ? result.order.id : payload.orderId);
    } catch (error) {
      alert(error.message || (isSpanishPage() ? 'Ocurrió un error, intenta de nuevo' : 'حدث خطأ، يرجى المحاولة مرة أخرى'));
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = isSpanishPage() ? 'Confirmar pedido — Pago contra entrega' : 'تاكيد الطلب';
      }
    }
  });

  function initLazyVideos() {
    function startVideo(video) {
      if (video.dataset.src) {
        video.src = video.dataset.src;
        video.removeAttribute('data-src');
      }
      if (!video.getAttribute('src')) return;
      video.preload = 'auto';
      if (video.readyState === 0) video.load();

      function tryPlay() {
        if (video.autoplay) video.play().catch(function () {});
      }

      if (video.readyState >= 2) {
        tryPlay();
        return;
      }

      video.addEventListener('loadeddata', tryPlay, { once: true });
      video.addEventListener('canplay', tryPlay, { once: true });
    }

    var ugcVideos = Array.prototype.slice.call(document.querySelectorAll('#video-testimonials .ugc-rail .js-lazy-video'));
    ugcVideos.slice(0, 2).forEach(startVideo);

    var lazyVideos = Array.prototype.slice.call(document.querySelectorAll('.js-lazy-video[data-src]'));
    if (!lazyVideos.length) return;

    if ('IntersectionObserver' in window) {
      var videoObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          startVideo(entry.target);
          videoObserver.unobserve(entry.target);
        });
      }, { rootMargin: '800px 0px', threshold: 0.01 });
      lazyVideos.forEach(function (video) { videoObserver.observe(video); });
      return;
    }

    lazyVideos.forEach(startVideo);
  }

  initLazyVideos();

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.js-open-order')) return;
    trackFacebookInitiateCheckout();
    trackTikTokInitiateCheckout();
  }, true);
});
