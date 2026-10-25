# Verify emails in Clay

Clean or score an email column in a Clay table with an **HTTP API** enrichment. One GET call per row.

## Add the enrichment

1. In your table, add a column, choose **HTTP API** (under "Make an API call" / Integrations).
2. Set it up:
   - **Method:** `GET`
   - **URL:** `https://happy.mailtester.ninja/ninja?email={{Email}}&key=YOUR_KEY`
     - Map `{{Email}}` to your email column.
     - Replace `YOUR_KEY` with your [paid key](https://mailtester.ninja/verify-emails-unlimited/), or a [free token](https://mailtester.ninja/free-email-verification-api/) to try it on a few rows (50 checks a day, one request every 30 seconds). Store it in a Clay secret if your workspace supports it.
3. Run the column. Clay stores the JSON response.

## Use the result

Add formula columns that read the response:
- `code` : `ok` valid, `ko` invalid, `mb` uncertain (catch-all).
- `message` : the readable label.

Then filter the table on `code = ok`, or write back to your CRM only the rows that pass.

## Where it fits

Clay is often the last step before outreach. Build the address with your source (or our [email finder](https://mailtester.ninja/email-finder/)), verify it here, then push only deliverable contacts to your sequencer. Fewer bounces, better sender reputation.

## Rate and credits

Each row is one request. For big tables, let Clay pace the run; keep in mind the plan rate (Pro 11 req/10s, Ultimate 23 req/10s) and buy a quantity at checkout to go faster.

## Free tier

Avoid `key=free` in Clay: its servers share their IP addresses with all its users, and the keyless tier is counted per IP. With a free token, space calls by 30 seconds: on the free tier the API answers HTTP 429 when you call too fast or reach the daily limit, and that answer is not a verdict. A paid key removes the wait.

Docs: https://mailtester.ninja/api/
