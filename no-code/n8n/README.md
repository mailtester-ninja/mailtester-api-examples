# Verify emails in n8n

Add real time email verification to any n8n workflow with a single **HTTP Request** node. No custom code.

## Quick setup (HTTP Request node)

1. Add an **HTTP Request** node.
2. Configure it:
   - **Method:** `GET`
   - **URL:** `https://happy.mailtester.ninja/ninja`
   - **Send Query Parameters:** on
     - `email` = `{{ $json.email }}` (map to your field)
     - `key` = your [paid key](https://mailtester.ninja/verify-emails-unlimited/), or a [free token](https://mailtester.ninja/free-email-verification-api/) to try it (50 checks a day, one request every 30 seconds)
3. The node returns the JSON response. Read `{{ $json.code }}`:
   - `ok` valid and deliverable
   - `ko` invalid, will bounce
   - `mb` uncertain (catch-all or unprobeable)

## Keep your key secret

Create a **Header Auth** or **Generic Credential**, or store the key in an n8n variable, instead of pasting it into the node. Never commit a workflow with the key inlined.

## Branch on the verdict

Add an **IF** node after the HTTP Request:
- Condition: `{{ $json.code }}` equals `ok`
- True branch: add to your mailing list / continue.
- False branch: skip, tag, or send to review.

## Respect the rate limit

For lists, add a **Loop Over Items** (batch size 1) plus a **Wait** node (about 1 second on Pro, 0.45s on Ultimate), or use the node's built in batching. Pro = 11 req/10s, Ultimate = 23 req/10s.

## Importable workflow

[`workflow.json`](workflow.json) in this folder is a minimal, importable n8n workflow: a manual trigger, the HTTP Request node pre-filled, and an IF node that splits valid from invalid. Import it via **n8n > Workflows > Import from File**, then set your key (a paid key, or a free token to try it).

## Free tier

Avoid `key=free` in n8n cloud: its servers share their IP addresses with all its users, and the keyless tier is counted per IP. With a free token, space calls by 30 seconds: on the free tier the API answers HTTP 429 when you call too fast or reach the daily limit, and that answer is not a verdict. A paid key removes the wait.

Docs: https://mailtester.ninja/api/
