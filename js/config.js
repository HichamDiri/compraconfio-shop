// Orders post to Google Apps Script (and /api/orders on Vercel as primary path).
window.GOOGLE_SHEETS_URL = 'https://script.google.com/macros/s/AKfycbx__S60obOiYJB7dqlBNMqIvaxTIzY2pafz92tsgYX9G7tpGZvMQYur-N664u787IZVHw/exec';
window.ORDER_API_URL = '/api/orders';

// Per-funnel Web App URLs (deploy orders.gs from each spreadsheet).
// Paste your new sheet /exec URL for car-solar-alarm-led-panama-meta below.
window.GOOGLE_SHEETS_BY_SOURCE = {
  'car-solar-alarm-led-panama-meta': ''
};

window.resolveGoogleSheetsUrl = function (source) {
  var key = String(source || '').trim();
  if (key && window.GOOGLE_SHEETS_BY_SOURCE &&
      Object.prototype.hasOwnProperty.call(window.GOOGLE_SHEETS_BY_SOURCE, key)) {
    return window.GOOGLE_SHEETS_BY_SOURCE[key] || '';
  }
  if (document.body && document.body.dataset.googleSheetsUrl) {
    return document.body.dataset.googleSheetsUrl;
  }
  return window.GOOGLE_SHEETS_URL || '';
};

window.hasGoogleSheetsEndpoint = function (source) {
  if (window.ORDER_API_URL) return true;
  return Boolean(window.resolveGoogleSheetsUrl(source));
};

(function flushAbandonDraftFromConfig() {
  var DRAFT_KEY = 'cc_abandon_draft';
  var STORAGE_PREFIX = 'cc_abandon_sent_';

  var raw;
  try {
    raw = localStorage.getItem(DRAFT_KEY);
  } catch (error) {
    return;
  }
  if (!raw) return;

  try {
    var payload = JSON.parse(raw);
    if (!payload || !payload.phone) return;
    var key = STORAGE_PREFIX + payload.source + '_' + payload.phone;
    if (sessionStorage.getItem(key) === '1') {
      localStorage.removeItem(DRAFT_KEY);
      return;
    }
    var sheetsUrl = window.resolveGoogleSheetsUrl(payload.source);
    if (!sheetsUrl) return;
    sessionStorage.setItem(key, '1');
    localStorage.removeItem(DRAFT_KEY);
    var body = 'payload=' + encodeURIComponent(JSON.stringify(payload));
    if (typeof navigator.sendBeacon === 'function') {
      navigator.sendBeacon(
        sheetsUrl,
        new Blob([body], { type: 'application/x-www-form-urlencoded;charset=UTF-8' })
      );
    }
  } catch (error) {
    try {
      localStorage.removeItem(DRAFT_KEY);
    } catch (removeError) {}
  }
})();
