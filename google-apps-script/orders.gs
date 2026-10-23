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
var COL_MONEDA = 16;
var COL_FUENTE = 17;
var COL_PRODUCT_PAGE = 19;
var COL_COUNTRY = 20;

var SITE_URL = 'https://www.compraconfio.shop/';

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
  'Country'
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
    message: 'CompraConfio order endpoint v20261023-page-country is running.'
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

function amountNumberFormat_(value) {
  return Number(value) % 1 === 0 ? '0' : '0.00';
}

function setPlainAmount_(sheet, row, col, value) {
  var n = Number(value) || 0;
  var cell = sheet.getRange(row, col);
  cell.setNumberFormat(amountNumberFormat_(n));
  cell.setValue(n);
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
  var country = countryLabel_(data.marketCountry || inferCountry_(data), currency);
  var productPage = data.productPage || productPageFromSource_(data.source);
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
    country
  ]);

  var row = sheet.getLastRow();
  setPlainAmount_(sheet, row, COL_SUBTOTAL, subtotal);
  setPlainAmount_(sheet, row, COL_SHIPPING, shippingDisplay);
  setPlainAmount_(sheet, row, COL_TOTAL, total);
}

function inferCountry_(data) {
  var c = String(data.country || '').toLowerCase();
  if (c.indexOf('panam') >= 0) return 'panama';
  if (c.indexOf('guatem') >= 0) return 'guatemala';
  return c || '';
}

function countryLabel_(value, currency) {
  var c = String(value || '').toLowerCase();
  if (c.indexOf('panam') >= 0 || c === 'pa') return 'Panamá';
  if (c.indexOf('guatem') >= 0 || c === 'gt') return 'Guatemala';
  if (!c) {
    var cur = String(currency || '').toUpperCase();
    if (cur === 'USD') return 'Panamá';
    if (cur === 'GTQ') return 'Guatemala';
  }
  return value || '';
}

function productPageFromSource_(source) {
  var s = String(source || '').trim();
  if (!s || s === 'deploy-check' || s === 'compraconfio') return '';
  return SITE_URL + s;
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
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    return;
  }

  [COL_PRODUCT_PAGE, COL_COUNTRY].forEach(function (col) {
    var cell = sheet.getRange(1, col);
    if (cell.getValue() !== HEADERS[col - 1]) {
      cell.setValue(HEADERS[col - 1]).setFontWeight('bold');
    }
  });
}

/**
 * Run once from the Apps Script editor to turn old "Q39" / "$42,00" amounts into plain numbers.
 */
function fixExistingPedidosAmountFormats() {
  var sheet = getSheet_();
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  for (var row = 2; row <= lastRow; row++) {
    [COL_SUBTOTAL, COL_SHIPPING, COL_TOTAL].forEach(function (col) {
      var raw = sheet.getRange(row, col).getValue();
      if (raw === '' || raw == null) return;
      var n = typeof raw === 'number' ? raw : normalizeAmount_(raw);
      if (typeof n === 'number' && !isNaN(n)) {
        setPlainAmount_(sheet, row, col, n);
      }
    });
  }
}

/**
 * Run once from the Apps Script editor to add the headers and fill Product page / Country on old rows.
 */
function backfillProductPageAndCountry() {
  var sheet = getSheet_();
  ensureHeaders_(sheet);
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  for (var row = 2; row <= lastRow; row++) {
    var pageCell = sheet.getRange(row, COL_PRODUCT_PAGE);
    var countryCell = sheet.getRange(row, COL_COUNTRY);
    if (!pageCell.getValue()) {
      pageCell.setValue(productPageFromSource_(sheet.getRange(row, COL_FUENTE).getValue()));
    }
    if (!countryCell.getValue()) {
      countryCell.setValue(countryLabel_('', sheet.getRange(row, COL_MONEDA).getValue()));
    }
  }
}

function jsonOutput_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
