/**
 * CompraConfio — Google Sheets order receiver
 *
 * Setup:
 * 1. Create a Google Sheet (e.g. "CompraConfio Pedidos")
 * 2. Extensions → Apps Script → paste this file → Save
 * 3. Deploy → New deployment → Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 4. Copy the Web App URL into js/config.js → GOOGLE_SHEETS_URL
 */

var SHEET_NAME = 'Pedidos';

var HEADERS = [
  'Fecha',
  'N° Pedido',
  'Nombre',
  'WhatsApp',
  'Departamento',
  'Municipio',
  'Dirección',
  'Zona/Colonia',
  'Producto',
  'Oferta',
  'Color',
  'Subtotal',
  'Envío',
  'Método envío',
  'Total',
  'Moneda',
  'Fuente',
  'Estado'
];

function doPost(e) {
  try {
    var data = parsePayload_(e);
    appendOrder_(data);
    return jsonOutput_({ ok: true });
  } catch (err) {
    return jsonOutput_({ ok: false, message: String(err) });
  }
}

function doGet() {
  return jsonOutput_({ ok: true, message: 'CompraConfio order endpoint is running.' });
}

function parsePayload_(e) {
  if (!e || !e.postData || !e.postData.contents) {
    throw new Error('Missing POST body');
  }

  var raw = e.postData.contents;
  var parsed;

  if (e.postData.type === 'application/json') {
    parsed = JSON.parse(raw);
  } else if (raw.indexOf('payload=') === 0) {
    parsed = JSON.parse(decodeURIComponent(raw.replace(/^payload=/, '').replace(/\+/g, ' ')));
  } else {
    parsed = JSON.parse(raw);
  }

  return parsed && typeof parsed === 'object' ? parsed : {};
}

function appendOrder_(data) {
  var sheet = getSheet_();
  ensureHeaders_(sheet);

  var shipping = data.shipping ? 'Q' + data.shipping : 'Gratis';
  var total = data.total || data.price || '';
  var createdAt = data.createdAt ? new Date(data.createdAt) : new Date();

  sheet.appendRow([
    createdAt,
    data.orderId || '',
    data.name || '',
    data.phone || '',
    data.department || '',
    data.city || '',
    data.addressLine || data.address || '',
    data.zone || '',
    data.productName || '',
    data.bundleLabel || '',
    data.color || '',
    data.price ? 'Q' + data.price : '',
    shipping,
    data.shippingMethod || 'Envío gratis',
    total ? 'Q' + total : '',
    data.currency || 'GTQ',
    data.source || '',
    'Nuevo'
  ]);
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }

  return sheet;
}

function ensureHeaders_(sheet) {
  if (sheet.getLastRow() > 0) {
    return;
  }

  sheet.appendRow(HEADERS);
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
}

function jsonOutput_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
