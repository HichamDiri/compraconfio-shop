// Orders post directly to Google Apps Script (avoids /api/orders HTML errors on Vercel).
window.GOOGLE_SHEETS_URL = 'https://script.google.com/macros/s/AKfycbx__S60obOiYJB7dqlBNMqIvaxTIzY2pafz92tsgYX9G7tpGZvMQYur-N664u787IZVHw/exec';
window.ORDER_API_URL = '/api/orders';

(function flushAbandonDraftFromConfig() {
  var DRAFT_KEY = 'cc_abandon_draft';
  var STORAGE_PREFIX = 'cc_abandon_sent_';

  if (!window.GOOGLE_SHEETS_URL) return;

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
    sessionStorage.setItem(key, '1');
    localStorage.removeItem(DRAFT_KEY);
    var body = 'payload=' + encodeURIComponent(JSON.stringify(payload));
    if (typeof navigator.sendBeacon === 'function') {
      navigator.sendBeacon(
        window.GOOGLE_SHEETS_URL,
        new Blob([body], { type: 'application/x-www-form-urlencoded;charset=UTF-8' })
      );
    }
  } catch (error) {
    try {
      localStorage.removeItem(DRAFT_KEY);
    } catch (removeError) {}
  }
})();
