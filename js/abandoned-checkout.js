(function () {
  var STORAGE_PREFIX = 'cc_abandon_sent_';
  var DRAFT_KEY = 'cc_abandon_draft';

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.body || document.body.dataset.abandonCheckout !== 'on') return;

    var form = document.getElementById('orderForm');
    if (!form || !window.GOOGLE_SHEETS_URL) return;

    var submitted = false;

    function normalizePanamaPhone(value) {
      var digits = String(value || '').replace(/[^\d]/g, '');
      if (/^507[2-9][0-9]{7}$/.test(digits)) return digits.slice(3);
      if (/^[2-9][0-9]{7}$/.test(digits)) return digits;
      return '';
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
      if (!normalizePanamaPhone(phone && phone.value)) return false;
      if (!department || !department.value.trim()) return false;
      if (!city || city.disabled || !city.value.trim()) return false;
      if (!addressLine || !addressLine.value.trim()) return false;

      return true;
    }

    function buildPayload() {
      mergeFields();
      var formData = new FormData(form);
      var bundle = form.querySelector('input[name="bundleOption"]:checked');
      var phone = normalizePanamaPhone(formData.get('phone'));
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
        status: 'Abandono'
      };
    }

    function storageKey(payload) {
      return STORAGE_PREFIX + payload.source + '_' + payload.phone;
    }

    function postPayload(payload) {
      var body = 'payload=' + encodeURIComponent(JSON.stringify(payload));

      return fetch(window.GOOGLE_SHEETS_URL, {
        method: 'POST',
        mode: 'no-cors',
        keepalive: true,
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        body: body
      }).catch(function () {});
    }

    function saveDraft() {
      if (submitted || !isComplete()) {
        try {
          localStorage.removeItem(DRAFT_KEY);
        } catch (error) {}
        return;
      }

      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(buildPayload()));
      } catch (error) {}
    }

    function sendAbandon() {
      if (submitted) return;

      saveDraft();

      var payload;
      try {
        payload = isComplete() ? buildPayload() : JSON.parse(localStorage.getItem(DRAFT_KEY) || 'null');
      } catch (error) {
        payload = null;
      }

      if (!payload || !payload.phone || sessionStorage.getItem(storageKey(payload)) === '1') return;

      sessionStorage.setItem(storageKey(payload), '1');
      postPayload(payload);
    }

    form.addEventListener('input', saveDraft, true);
    form.addEventListener('change', saveDraft, true);

    form.addEventListener('submit', function () {
      if (isComplete()) submitted = true;
      try {
        localStorage.removeItem(DRAFT_KEY);
      } catch (error) {}
    }, true);

    document.querySelectorAll('[data-close-order]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        window.setTimeout(saveDraft, 0);
      });
    });

    document.addEventListener('click', function (event) {
      var link = event.target.closest('a[href]');
      if (!link) return;
      if (link.target === '_blank' || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

      var href = link.getAttribute('href');
      if (!href || href.charAt(0) === '#' || href.indexOf('javascript:') === 0 || href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) {
        return;
      }

      sendAbandon();
    }, true);

    window.addEventListener('pagehide', sendAbandon);
  });
})();
