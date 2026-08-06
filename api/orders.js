const GOOGLE_SHEETS_URL =
  process.env.GOOGLE_SHEETS_URL ||
  'https://script.google.com/macros/s/AKfycbx__S60obOiYJB7dqlBNMqIvaxTIzY2pafz92tsgYX9G7tpGZvMQYur-N664u787IZVHw/exec';

function readPayload(req) {
  if (!req.body) return {};
  if (typeof req.body === 'string') {
    try {
      return JSON.parse(req.body);
    } catch (error) {
      return {};
    }
  }
  return req.body;
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, message: 'Method not allowed' });
  }

  try {
    const payload = readPayload(req);
    const encoded = new URLSearchParams();
    encoded.append('payload', JSON.stringify(payload));

    const response = await fetch(GOOGLE_SHEETS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: encoded.toString(),
      redirect: 'follow'
    });

    const text = await response.text();
    let result = null;

    try {
      result = JSON.parse(text);
    } catch (error) {
      return res.status(502).json({
        ok: false,
        message: 'Google Sheets returned an unexpected response',
        detail: text.slice(0, 300),
        status: response.status
      });
    }

    if (!response.ok || !result.ok) {
      return res.status(502).json({
        ok: false,
        message: result.message || 'Google Sheets rejected the order',
        detail: text.slice(0, 300),
        status: response.status
      });
    }

    return res.status(200).json({
      ok: true,
      order: { id: payload.orderId || '' }
    });
  } catch (error) {
    return res.status(500).json({
      ok: false,
      message: error.message || 'Failed to save order'
    });
  }
};
