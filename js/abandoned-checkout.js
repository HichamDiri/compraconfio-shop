(function () {
  var ABANDON_DELAY_MS = 5 * 60 * 1000;
  var STORAGE_PREFIX = 'cc_abandon_sent_';

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.body || document.body.dataset.abandonCheckout !== 'on') return;

    var form = document.getElementById('orderForm');
    if (!form || !window.GOOGLE_SHEETS_URL) return;

    var eligible = false;
    var submitted = false;
    var sent = false;
    var abandonTimer = null;

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
      if (!form.checkValidity()) return false;
      var phone = form.querySelector('#phone');
      return Boolean(normalizePanamaPhone(phone && phone.value));
    }

    function clearTimer() {
      eligible = false;
      if (abandonTimer) {
        clearTimeout(abandonTimer);
        abandonTimer = null;
      }
    }

    function scheduleEligibility() {
      clearTimer();
      if (submitted || sent || !isComplete()) return;

      abandonTimer = setTimeout(function () {
        if (!submitted && !sent && isComplete()) {
          eligible = true;
        }
      }, ABANDON_DELAY_MS);
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

    function sendAbandon() {
      if (sent || submitted || !eligible || !isComplete()) return;

      var payload = buildPayload();
      if (!payload.phone || sessionStorage.getItem(storageKey(payload)) === '1') return;

      var body = new URLSearchParams();
      body.append('payload', JSON.stringify(payload));

      var delivered = typeof navigator.sendBeacon === 'function'
        && navigator.sendBeacon(window.GOOGLE_SHEETS_URL, body);

      if (!delivered) {
        fetch(window.GOOGLE_SHEETS_URL, {
          method: 'POST',
          mode: 'no-cors',
          keepalive: true,
          body: body
        });
      }

      sent = true;
      sessionStorage.setItem(storageKey(payload), '1');
    }

    form.addEventListener('input', scheduleEligibility, true);
    form.addEventListener('change', scheduleEligibility, true);

    form.addEventListener('submit', function () {
      if (form.checkValidity()) submitted = true;
    }, true);

    window.addEventListener('pagehide', sendAbandon);
  });
})();
