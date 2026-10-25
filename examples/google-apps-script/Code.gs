/**
 * MailTester Ninja for Google Sheets, via Apps Script.
 *
 * Setup:
 *   1. In your Sheet: Extensions > Apps Script, paste this file.
 *   2. Project Settings > Script Properties: add MAILTESTER_KEY = your key.
 *      To try it free, use a free token (50 checks a day, one request every 30 s):
 *        https://mailtester.ninja/free-email-verification-api/
 *      key=free does not suit Sheets: Google's servers share their IP addresses,
 *      and the keyless tier is counted per IP.
 *      Paid key (full speed): https://mailtester.ninja/verify-emails-unlimited/
 *   3. Back in the Sheet, use the custom function:  =MT_VERIFY(A2)
 *      or run verifyColumn() from the Apps Script editor for a whole column.
 */

var ENDPOINT = 'https://happy.mailtester.ninja/ninja';

function getKey_() {
  var key = PropertiesService.getScriptProperties().getProperty('MAILTESTER_KEY');
  if (!key) throw new Error('Set MAILTESTER_KEY in Script Properties: a free token from https://mailtester.ninja/free-email-verification-api/ or a paid key from https://mailtester.ninja/verify-emails-unlimited/');
  return key;
}

function verifyOne_(email) {
  var url = ENDPOINT + '?email=' + encodeURIComponent(email) + '&key=' + encodeURIComponent(getKey_());
  var resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  if (resp.getResponseCode() === 429) {
    var lim = JSON.parse(resp.getContentText());
    return { code: 'error', message: 'Free limit: ' + lim.message };
  }
  if (resp.getResponseCode() !== 200) return { code: 'error', message: 'HTTP ' + resp.getResponseCode() };
  return JSON.parse(resp.getContentText());
}

/**
 * Custom function:  =MT_VERIFY("someone@example.com")
 * Returns the human readable verdict (Accepted, Rejected, Catch-All, ...).
 * Note: Sheets caches custom function results; edit the cell to refresh.
 */
function MT_VERIFY(email) {
  if (!email) return '';
  return verifyOne_(email).message || '';
}

/**
 * Verify column A (from row 2), writing code to B and message to C.
 * Respects the rate limit with a pause between calls.
 */
function verifyColumn() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var last = sheet.getLastRow();
  for (var row = 2; row <= last; row++) {
    var email = sheet.getRange(row, 1).getValue();
    if (!email) continue;
    var r = verifyOne_(String(email).trim());
    sheet.getRange(row, 2).setValue(r.code || '');
    sheet.getRange(row, 3).setValue(r.message || '');
    Utilities.sleep(getKey_().indexOf('mtf_') === 0 ? 30000 : 1000); // 30 s on a free token, ~1 s on Pro
  }
}
