/**
 * CompraConfio ? Google Sheets order receiver
 *
 * Deploy from the spreadsheet "CompraConfio Pedidos" (tab "Pedidos"):
 * Extensions ? Apps Script ? paste ? Deploy ? Web app (Execute as: Me, Anyone)
 * Copy the /exec URL into js/config.js ? GOOGLE_SHEETS_BY_SOURCE or GOOGLE_SHEETS_URL
 */

var SHEET_NAME = 'Pedidos';

/** Column indexes (1-based) ? must match HEADERS */
var COL_SUBTOTAL = 12;
var COL_SHIPPING = 13;
var COL_TOTAL = 15;

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
  'Estado',
  'Product page',
  '',
  'country',
  'currency'
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
  return jsonOutput_({
    ok: true,
    message: 'CompraConfio order endpoint v20261023-usd-format is running.'
  });
}

function parsePayload_(e) {
  if (e && e.parameter && e.parameter.payload) {
    return JSON.parse(String(e.parameter.payload));
  }

  if (!e || !e.postData || !e.postData.contents) {
    throw new Error('Missing POST body');
  }

  var raw = e.postData.contents;
  var parsed;

  if (e.postData.type === 'application/json' || e.postData.type === 'text/plain') {
    parsed = JSON.parse(raw);
  } else if (raw.indexOf('payload=') >= 0) {
    var match = raw.match(/(?:^|&)payload=([^&]*)/);
    if (!match) {
      throw new Error('Missing payload field');
    }
    parsed = JSON.parse(decodeURIComponent(match[1].replace(/\+/g, ' ')));
  } else {
    parsed = JSON.parse(raw);
  }

  return parsed && typeof parsed === 'object' ? parsed : {};
}

function normalizeAmount_(value) {
  if (value == null || value === '') return '';
  var s = String(value).trim().replace(/^\s*([$Qq]|USD|GTQ)\s*/i, '');
  s = s.replace(/,/g, '');
  var n = Number(s);
  if (!isNaN(n)) return n;
  return s;
}

function amountNumberFormat_(currency) {
  var c = String(currency || '').toUpperCase();
  if (c === 'USD') return '$#,##0.00';
  if (c === 'GTQ') return '#,##0.00';
  return '#,##0.00';
}

function applyAmountFormats_(sheet, row, currency) {
  if (!row || row < 2) return;
  var fmt = amountNumberFormat_(currency);
  sheet.getRange(row, COL_SUBTOTAL).setNumberFormat(fmt);
  sheet.getRange(row, COL_SHIPPING).setNumberFormat(fmt);
  sheet.getRange(row, COL_TOTAL).setNumberFormat(fmt);
}

function appendOrder_(data) {
  var sheet = getSheet_();
  ensureHeaders_(sheet);

  var shippingDisplay = normalizeAmount_(data.shipping != null && data.shipping !== '' ? data.shipping : 0);
  if (shippingDisplay === '') shippingDisplay = 0;
  var subtotal = normalizeAmount_(data.price);
  var total = normalizeAmount_(data.total != null && data.total !== '' ? data.total : data.price);
  var currency = String(data.currency || data.marketCurrency || 'GTQ').toUpperCase();
  var moneda = currency;
  var marketCountry = data.marketCountry || inferCountry_(data);
  var productPage = data.productPage || '';
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
    subtotal,
    shippingDisplay,
    data.shippingMethod || 'Envío gratis',
    total,
    moneda,
    data.source || '',
    data.status || 'Nuevo',
    productPage,
    '',
    marketCountry,
    currency
  ]);

  var row = sheet.getLastRow();
  applyAmountFormats_(sheet, row, currency);
  sheet.getRange(row, COL_SUBTOTAL).setValue(Number(subtotal) || 0);
  sheet.getRange(row, COL_SHIPPING).setValue(Number(shippingDisplay) || 0);
  sheet.getRange(row, COL_TOTAL).setValue(Number(total) || 0);
}

function inferCountry_(data) {
  var c = String(data.country || '').toLowerCase();
  if (c.indexOf('panam') >= 0) return 'panama';
  if (c.indexOf('guatem') >= 0) return 'guatemala';
  return c || '';
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
  sheet.getRange(2, COL_SUBTOTAL, sheet.getMaxRows() - 1, 1).setNumberFormat('#,##0.00');
  sheet.getRange(2, COL_SHIPPING, sheet.getMaxRows() - 1, 1).setNumberFormat('#,##0.00');
  sheet.getRange(2, COL_TOTAL, sheet.getMaxRows() - 1, 1).setNumberFormat('#,##0.00');
}

/**
 * Run once from Apps Script editor (Run) to remove column-wide "Q" display on old rows.
 * Re-formats Subtotal / Envío / Total from Moneda column (col 16).
 */
function fixExistingPedidosAmountFormats() {
  var sheet = getSheet_();
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  for (var row = 2; row <= lastRow; row++) {
    var currency = String(sheet.getRange(row, 16).getValue() || 'GTQ').toUpperCase();
    applyAmountFormats_(sheet, row, currency);
    [COL_SUBTOTAL, COL_SHIPPING, COL_TOTAL].forEach(function (col) {
      var cell = sheet.getRange(row, col);
      var n = normalizeAmount_(cell.getDisplayValue());
      if (typeof n === 'number' && !isNaN(n)) {
        cell.setValue(n);
      }
    });
  }
}

function jsonOutput_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
