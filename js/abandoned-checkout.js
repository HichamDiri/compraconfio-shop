(function () {
  var STORAGE_PREFIX = 'cc_abandon_sent_';
  var DRAFT_KEY = 'cc_abandon_draft';

  function storageKey(payload) {
    return STORAGE_PREFIX + payload.source + '_' + payload.phone;
  }

  function resolveSheetsUrl(source) {
    if (typeof window.resolveGoogleSheetsUrl === 'function') {
      return window.resolveGoogleSheetsUrl(source || '');
    }
    return window.GOOGLE_SHEETS_URL || '';
  }

  function postPayload(payload, useBeacon) {
    var url = resolveSheetsUrl(payload && payload.source);
    if (!url) return Promise.resolve(false);

    var encoded = 'payload=' + encodeURIComponent(JSON.stringify(payload));

    if (useBeacon && typeof navigator.sendBeacon === 'function') {
      var blob = new Blob([encoded], { type: 'application/x-www-form-urlencoded;charset=UTF-8' });
      if (navigator.sendBeacon(url, blob)) {
        return Promise.resolve(true);
      }
    }

    if (window.ORDER_API_URL) {
      return fetch(window.ORDER_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify(payload)
      }).then(function (response) {
        return response.ok;
      }).catch(function () {
        return false;
      });
    }

    return fetch(url, {
      method: 'POST',
      mode: 'no-cors',
      keepalive: true,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: encoded
    }).then(function () {
      return true;
    }).catch(function () {
      if (useBeacon && typeof navigator.sendBeacon === 'function') {
        var fallbackBlob = new Blob([encoded], { type: 'application/x-www-form-urlencoded;charset=UTF-8' });
        return navigator.sendBeacon(url, fallbackBlob);
      }
      return false;
    });
  }

  function flushSavedDraft() {
    if (!window.GOOGLE_SHEETS_URL && !window.ORDER_API_URL) return;

    var raw;
    try {
      raw = localStorage.getItem(DRAFT_KEY);
    } catch (error) {
      return;
    }
    if (!raw) return;

    try {
      var payload = JSON.parse(raw);
      if (!payload || !payload.phone || sessionStorage.getItem(storageKey(payload)) === '1') {
        localStorage.removeItem(DRAFT_KEY);
        return;
      }
      sessionStorage.setItem(storageKey(payload), '1');
      localStorage.removeItem(DRAFT_KEY);
      postPayload(payload, true);
    } catch (error) {
      try {
        localStorage.removeItem(DRAFT_KEY);
      } catch (removeError) {}
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    flushSavedDraft();

    if (!document.body || document.body.dataset.abandonCheckout !== 'on') return;

    var form = document.getElementById('orderForm');
    if (!form || (!window.GOOGLE_SHEETS_URL && !window.ORDER_API_URL)) return;

    var submitted = false;
    var sending = false;
    var idleMinutes = parseFloat(document.body.dataset.abandonIdleMinutes || '', 10);
    var idleMs = idleMinutes > 0 ? Math.round(idleMinutes * 60 * 1000) : 0;
    var idleTimer = null;

    function clearIdleTimer() {
      if (idleTimer) {
        clearTimeout(idleTimer);
        idleTimer = null;
      }
    }

    var marketCountry = document.body.dataset.country || 'PA';

    function normalizePanamaPhone(value) {
      var digits = String(value || '').replace(/[^\d]/g, '');
      if (/^507[2-9][0-9]{7}$/.test(digits)) return digits.slice(3);
      if (/^[2-9][0-9]{7}$/.test(digits)) return digits;
      if (/^507[2-9][0-9]{6}$/.test(digits)) return digits.slice(3);
      if (/^[2-9][0-9]{6}$/.test(digits)) return digits;
      return '';
    }

    function normalizeGuatemalaPhone(value) {
      var digits = String(value || '').replace(/[^\d]/g, '');
      if (/^502[34567][0-9]{7}$/.test(digits)) return digits.slice(3);
      if (/^[34567][0-9]{7}$/.test(digits)) return digits;
      return '';
    }

    function normalizeCheckoutPhone(value) {
      if (marketCountry === 'GT') return normalizeGuatemalaPhone(value);
      return normalizePanamaPhone(value);
    }

    function capturePhone(value) {
      var strict = normalizeCheckoutPhone(value);
      if (strict) return strict;
      var digits = String(value || '').replace(/[^\d]/g, '');
      return digits.length >= 7 && digits.length <= 15 ? digits : '';
    }

    function mergeFields() {
      var firstName = form.querySelector('#firstName');
      var lastName = form.querySelector('#lastName');
      var name = form.querySelector('#name');
      var addressLine = form.querySelector('#addressLine');
      var zone = form.querySelector('#zone');
      var address = form.querySelector('#address');

      if (name && firstName && lastName) {
        name.value = (firstName.value.trim() + ' ' + lastName.value.trim()).trim();
      }
      if (address && addressLine) {
        var zoneValue = zone ? zone.value.trim() : '';
        address.value = [addressLine.value.trim(), zoneValue].filter(Boolean).join(', ');
      }
    }

    function isComplete() {
      mergeFields();

      var firstName = form.querySelector('#firstName');
      var lastName = form.querySelector('#lastName');
      var phone = form.querySelector('#phone');
      var department = form.querySelector('#department');
      var city = form.querySelector('#city');
      var addressLine = form.querySelector('#addressLine');

      if (!firstName || !firstName.value.trim()) return false;
      if (!lastName || !lastName.value.trim()) return false;
      if (!capturePhone(phone && phone.value)) return false;
      if (!department || !department.value.trim()) return false;
      if (!city || city.disabled || !city.value.trim()) return false;
      if (!addressLine || !addressLine.value.trim()) return false;

      return true;
    }

    function hasLead() {
      mergeFields();
      var firstName = form.querySelector('#firstName');
      var name = form.querySelector('#name');
      var phone = form.querySelector('#phone');
      var hasName = (firstName && firstName.value.trim()) || (name && name.value.trim());
      return Boolean(hasName && capturePhone(phone && phone.value));
    }

    function buildPayload() {
      mergeFields();
      var formData = new FormData(form);
      var bundle = form.querySelector('input[name="bundleOption"]:checked');
      var phone = capturePhone(formData.get('phone'));
      var firstName = String(formData.get('firstName') || '').trim();
      var lastName = String(formData.get('lastName') || '').trim();
      var name = String(formData.get('name') || '').trim() || (firstName + ' ' + lastName).trim();
      var addressLine = String(formData.get('addressLine') || '').trim();
      var zone = String(formData.get('zone') || '').trim();
      var city = String(formData.get('city') || '').trim();
      var department = String(formData.get('department') || '').trim();
      var country = String(formData.get('country') || '').trim();
      var address = city;
      if (addressLine) address = address ? address + ', ' + addressLine : addressLine;
      if (department) address = address ? address + ', ' + department : department;
      if (country) address = address ? address + ', ' + country : country;

      return {
        orderId: 'CC-AB-' + Date.now().toString().slice(-8),
        productId: bundle ? String(bundle.dataset.productId || bundle.value || '').trim() : '',
        productName: bundle ? String(bundle.dataset.productName || '').trim() : '',
        price: bundle ? String(bundle.dataset.price || '').trim() : '',
        currency: String(formData.get('currency') || 'USD').trim(),
        name: name,
        firstName: firstName,
        lastName: lastName,
        phone: phone,
        address: address,
        addressLine: addressLine,
        zone: zone,
        city: city,
        country: country,
        department: department,
        bundleLabel: bundle ? String(bundle.dataset.label || '').trim() : '',
        shippingMethod: String(formData.get('shippingMethod') || '').trim(),
        shipping: String(formData.get('shipping') || '0').trim(),
        total: String(formData.get('total') || '').trim(),
        createdAt: new Date().toISOString(),
        source: String(formData.get('source') || '').trim(),
        status: 'Abandono',
        productPage: (document.body && document.body.dataset.productPage)
          ? document.body.dataset.productPage
          : (window.location.origin + window.location.pathname.replace(/\.html$/, '')),
        marketCountry: marketCountry === 'GT' ? 'guatemala' : (marketCountry === 'PA' ? 'panama' : String(marketCountry).toLowerCase()),
        marketCurrency: String(formData.get('currency') || 'USD').trim()
      };
    }

    function saveDraft() {
      if (submitted || !hasLead()) {
        try {
          localStorage.removeItem(DRAFT_KEY);
        } catch (error) {}
        return;
      }

      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(buildPayload()));
      } catch (error) {}
    }

    function syncIdleAbandonTimer() {
      clearIdleTimer();
      if (!idleMs || submitted) return;
      if (!hasLead()) return;
      idleTimer = setTimeout(function () {
        idleTimer = null;
        sendAbandon(false);
      }, idleMs);
    }

    function sendAbandon(useBeacon) {
      if (sending || submitted || !hasLead()) return;

      var payload = buildPayload();
      if (!payload.phone || sessionStorage.getItem(storageKey(payload)) === '1') return;

      sending = true;
      postPayload(payload, useBeacon).then(function (ok) {
        sending = false;
        if (!ok) return;
        sessionStorage.setItem(storageKey(payload), '1');
        try {
          localStorage.removeItem(DRAFT_KEY);
        } catch (error) {}
      });
    }

    function onFormActivity() {
      saveDraft();
      syncIdleAbandonTimer();
    }

    form.addEventListener('input', onFormActivity, true);
    form.addEventListener('change', onFormActivity, true);

    form.addEventListener('invalid', function () {
      sendAbandon(false);
    }, true);

    form.addEventListener('submit', function () {
      if (isComplete()) submitted = true;
      clearIdleTimer();
      try {
        localStorage.removeItem(DRAFT_KEY);
      } catch (error) {}
    }, true);

    window.addEventListener('pagehide', function () {
      sendAbandon(true);
    });

    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') sendAbandon(true);
    });

    window.ccCaptureLead = function () {
      sendAbandon(false);
    };

    document.addEventListener('click', function (event) {
      if (!event.target.closest('[data-close-order]')) return;
      setTimeout(function () {
        sendAbandon(false);
      }, 0);
    }, true);

    syncIdleAbandonTimer();
  });
})();
