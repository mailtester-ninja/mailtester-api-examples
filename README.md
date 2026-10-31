# MailTester Ninja API, examples for every stack

Real time email verification you can drop into any language, workflow tool or AI agent. One HTTP call tells you whether an email address is valid and deliverable, and we store nothing. A second endpoint, the Finder API, finds a person's work email from their name and company domain.

- **Website:** https://mailtester.ninja
- **API docs:** https://mailtester.ninja/api/
- **OpenAPI 3.1 spec:** https://mailtester.ninja/openapi.json (import into Postman, Swagger, Power Automate or an AI agent)
- **Free API token:** https://mailtester.ninja/free-email-verification-api/
- **Paid key:** https://mailtester.ninja/verify-emails-unlimited/
- **Try it free (web):** https://mailtester.ninja/email-verifier/

> The API is free to try: call it with `key=free` and no signup (10 checks a day), or get a [free token](https://mailtester.ninja/free-email-verification-api/) in one click (50 checks a day). For production use and higher volumes, a paid key removes the wait at some of the best prices on the market, with nothing stored.

---

## Official SDKs

| Language | Install | Package |
|----------|---------|---------|
| JavaScript and TypeScript | `npm install @mailtester-ninja/client` | [npm](https://www.npmjs.com/package/@mailtester-ninja/client) · [source](https://github.com/mailtester-ninja/mailtester-js) |
| Python | `pip install mailtester-ninja` | [PyPI](https://pypi.org/project/mailtester-ninja/) · [source](https://github.com/mailtester-ninja/mailtester-python) |

Both are typed, have no dependencies, pace list verification for you and raise clear errors (invalid key, limit reached). For other languages, the examples below wrap the same single call.

---

## Quickstart

One GET request, two parameters. Try it now, no signup:

```bash
curl "https://happy.mailtester.ninja/ninja?email=info@apple.com&key=free"
```

Then swap `free` for your free token or your paid key.

Response:

```json
{
  "email": "info@apple.com",
  "user": "Info",
  "domain": "apple.com",
  "mx": "mx-in.g.apple.com",
  "code": "ok",
  "message": "Accepted",
  "connections": 1
}
```

That is the whole API. Everything in this repo is that call, wrapped for your language or tool.

The JSON body is served as `text/plain` by default; send `Accept: application/json` to get `application/json`.

---

## The endpoint

```
GET https://happy.mailtester.ninja/ninja
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `email`   | yes | The email address to verify. URL encode it. |
| `key`     | yes | `free`, a free token (`mtf_...`), or your subscription key without the `{` and `}`. |

## Keys

| Access | Daily checks | Pace | `key` value |
|--------|--------------|------|-------------|
| No token | 10 per IP | 1 request every 30 s | `free` |
| [Free token](https://mailtester.ninja/free-email-verification-api/) | 50 per token | 1 request every 30 s | `mtf_...`, valid 7 days, renewable |
| [Paid plans](https://mailtester.ninja/verify-emails-unlimited/) | 100k to 200k+ | up to 23 requests per 10 s | your subscription key, sent by email right after checkout |

No-code tools (n8n cloud, Make, Zapier, Clay) and Google Sheets call from shared servers: use a free token there, since `key=free` is counted per IP.

## The response

| Field | Description |
|-------|-------------|
| `email` | The address you checked. |
| `user` | A human readable guess of the name, derived from the address. |
| `domain` | The domain part of the address. |
| `mx` | The mail server that answered, when there is one. |
| `code` | The machine readable verdict: `ok`, `ko` or `mb`, or `--` when there is no verdict (see below). |
| `message` | A human readable label for the verdict. |
| `connections` | Simultaneous connections currently used by your key. |

## Reading the verdict

Branch on `code`, show `message` to humans.

| `code` | Meaning | Typical `message` values | What to do |
|--------|---------|--------------------------|------------|
| `ok` | Valid and deliverable | `Accepted` | Safe to send. |
| `ko` | Invalid, will bounce | `Rejected`, `No MX` | Do not send. Drop it from your list. |
| `mb` | Maybe, cannot be confirmed | `Catch-All`, `MX Error`, `Timeout`, `SPAM Block`, `Unknown` | Uncertain. The domain accepts everything (catch-all) or the server could not be probed. Decide by risk. |
| `--` | No verdict, the address was not checked | `Invalid Key`, `Disabled Key`, or the free limit message (HTTP 429) | Fix the key, or wait and retry. Never drop the address on a `--`. |

We never guess "valid" on a catch-all domain. We label the uncertainty honestly so you keep control.

## Find a work email (Finder API)

A second endpoint finds a person's work email from their name and company domain. It needs a paid key.

```
GET https://happy.mailtester.ninja/find
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `first`   | yes | First name, for example `Jean-Pierre`. |
| `last`    | yes | Last name, for example `De La Tour`. |
| `domain`  | yes | Company domain, for example `example.com`. A website address or an email address at that domain works too. |
| `key`     | yes | Your subscription key, without the `{` and `}`. |

```bash
curl "https://happy.mailtester.ninja/find?first=Jane&last=Doe&domain=example.com&key=YOUR_KEY"
```

```json
{
  "code": "ok",
  "message": "Accepted",
  "found": true,
  "email": "jane.doe@example.com",
  "format": "first.last",
  "confidence": "high",
  "guess": null,
  "first": "Jane",
  "last": "Doe",
  "domain": "example.com",
  "mx": "mx.example.com",
  "permutations": 1,
  "tested": [
    { "email": "jane.doe@example.com", "code": "ok", "message": "Accepted" }
  ],
  "connections": 1,
  "limit": 100000,
  "rate": 1,
  "duration": 1.84,
  "reason": null
}
```

- MailTester Ninja tests the most common formats one by one, from the most frequent: `first.last`, `flast`, `first`, `firstlast`, `first_last`, `f.last`. Names are written the way mail servers expect them: lowercase, accents removed, hyphens kept, spaces removed (Jean-Pierre De La Tour gives `jean-pierre.delatour`).
- The search stops at the first address the mail server accepts, or when the answer applies to the whole domain. On a catch-all domain nothing can be confirmed, and `guess` holds the most common format.
- Personal email providers such as gmail.com are not searched (`message` is `Webmail`): an accepted address there could belong to anyone with the same name.
- `code`: `ok` found, `ko` not found, `mb` uncertain, `--` no answer (key problem or rate limit). `reason` explains, in plain English, why nothing was found.
- `format` is the pattern of the address returned (`first.last`, `flast`, `first`, `firstlast`, `first_last`, `f.last`): reuse it to verify colleagues at the same company with one verification each. `confidence` tells how sure the address is to belong to this person: `high` with the first and last name in it, `medium` with an initial (a namesake may share it), `low` with the first name only. `tested` lists every address checked, with its verdict.
- **Billing:** each format tested counts as one verification against your daily limit and your rate, even when nothing is found (`permutations`). The `/find` call itself is not counted.
- Over the rate of your key, the API answers HTTP 429 with a `Retry-After` header. One key can run up to 60 searches an hour on the same domain.

Ready to run: [`find.sh`](examples/curl/find.sh) (cURL), `find()` in the [Python](examples/python) and [Node.js](examples/nodejs) examples, `mailtester_find()` in the [PHP](examples/php) example.

## Rate limits

- **Free (`key=free` or a free token):** one request every 30 seconds. Over that pace, or past the daily limit, the API answers **HTTP 429** with `code` set to `--` and a JSON `message` saying how long to wait. A 429 is not a verdict: retry later, do not treat the address as invalid.
- **Pro:** 11 requests per 10 seconds (100k per day).
- **Ultimate:** 23 requests per 10 seconds (200k per day).
- Buy a quantity at checkout to multiply the rate, for example Ultimate x5 = 1M per day.
- **Finder API:** the same allowance. Each address format a search tests counts as one verification, and the search paces itself within the rate of your key.

For lists, verify sequentially or in small batches and respect the rate. Every example in this repo that loops includes throttling, 30 seconds between calls on the free tier.

---

## Pick your stack

### Languages
| | | | |
|---|---|---|---|
| [cURL](examples/curl) | [Python](examples/python) | [Node.js](examples/nodejs) | [PHP](examples/php) |
| [Go](examples/go) | [Ruby](examples/ruby) | [Java](examples/java) | [C#](examples/csharp) |
| [Google Apps Script (Sheets)](examples/google-apps-script) | | | |

### No code and automation
| | | | |
|---|---|---|---|
| [n8n](no-code/n8n) | [Make](no-code/make) | [Zapier](no-code/zapier) | [Clay](no-code/clay) |

### AI and agents
| | | |
|---|---|---|
| [MCP server (remote, official)](ai/mcp) | [Ready to use prompts](ai/prompts) | [OpenAI tool calling](ai/openai-tool-calling) |
| [Claude tool use](ai/claude-tool-use) | [LangChain tool](ai/langchain) | |

---

## Common patterns

**Clean a list:** verify each address, keep `ok`, drop `ko`, review `mb` by hand or by risk tolerance.

**Validate at signup:** verify on form submit, block `ko` in real time so bad addresses never enter your database.

**Enrich before outreach:** call the Finder API (or our [email finder](https://mailtester.ninja/email-finder/) on the web) with a name and a company domain: it returns an address the mail server has just accepted, ready to send.

## A note on privacy

MailTester Ninja verifies in real time and stores nothing. Addresses are processed in memory to return a verdict and are never saved, so there is nothing to leak and nothing to resell. Verification without a database.

## License

MIT, see [LICENSE](LICENSE). Use these examples freely in your own projects.

---

Built by [MailTester Ninja](https://mailtester.ninja). Questions? https://mailtester.ninja/contact/
