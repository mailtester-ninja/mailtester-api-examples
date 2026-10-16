# Verify emails in Google Sheets

Verify a column of emails right inside Google Sheets, with Apps Script. No server, no install.

## Setup

1. Open your Sheet, go to **Extensions > Apps Script**.
2. Paste [`Code.gs`](Code.gs).
3. **Project Settings > Script Properties**, add `MAILTESTER_KEY` = your key ([get one](https://mailtester.ninja/verify-emails-unlimited/)).
4. Save.

## Use it

- **Per cell formula:** `=MT_VERIFY(A2)` returns the verdict (Accepted, Rejected, Catch-All, ...).
- **Whole column:** run `verifyColumn()` from the editor. It reads column A (from row 2) and writes the code to B and the message to C, pausing to respect the rate limit.

> Sheets caches custom function results. Edit the cell to force a refresh.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
