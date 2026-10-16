# MailTester Ninja API, examples for every stack

Real time email verification you can drop into any language, workflow tool or AI agent. One HTTP call tells you whether an email address is valid and deliverable, and we store nothing.

- **Website:** https://mailtester.ninja
- **API docs:** https://mailtester.ninja/api/
- **Get a key:** https://mailtester.ninja/verify-emails-unlimited/
- **Try it free (web):** https://mailtester.ninja/email-verifier/

> Occasional checks are free on the website, no signup. For production use and higher volumes, a key unlocks the REST API at some of the best prices on the market, with nothing stored.

---

## Quickstart

One GET request, two parameters.

```bash
curl "https://happy.mailtester.ninja/ninja?email=info@apple.com&key=YOUR_KEY"
```

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

---

## The endpoint

```
GET https://happy.mailtester.ninja/ninja
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `email`   | yes | The email address to verify. URL encode it. |
| `key`     | yes | Your subscription key, without the `{` and `}`. |

Get your key at https://mailtester.ninja/verify-emails-unlimited/ , it arrives by email right after checkout.

## The response

| Field | Description |
|-------|-------------|
| `email` | The address you checked. |
| `user` | A human readable guess of the name, derived from the address. |
| `domain` | The domain part of the address. |
| `mx` | The mail server that answered, when there is one. |
| `code` | The machine readable verdict: `ok`, `ko` or `mb` (see below). |
| `message` | A human readable label for the verdict. |
| `connections` | Simultaneous connections currently used by your key. |

## Reading the verdict

Branch on `code`, show `message` to humans.

| `code` | Meaning | Typical `message` values | What to do |
|--------|---------|--------------------------|------------|
| `ok` | Valid and deliverable | `Accepted` | Safe to send. |
| `ko` | Invalid, will bounce | `Rejected`, `No MX` | Do not send. Drop it from your list. |
| `mb` | Maybe, cannot be confirmed | `Catch-All`, `MX Error`, `Timeout`, `SPAM Block`, `Unknown` | Uncertain. The domain accepts everything (catch-all) or the server could not be probed. Decide by risk. |

We never guess "valid" on a catch-all domain. We label the uncertainty honestly so you keep control.

## Rate limits

The key rate depends on your plan:

- **Pro:** 11 requests per 10 seconds (100k per day).
- **Ultimate:** 23 requests per 10 seconds (200k per day).
- Buy a quantity at checkout to multiply the rate, for example Ultimate x5 = 1M per day.

For lists, verify sequentially or in small batches and respect the rate. Every example in this repo that loops includes throttling.

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
| [Ready to use prompts](ai/prompts) | [OpenAI tool calling](ai/openai-tool-calling) | [Claude tool use](ai/claude-tool-use) |
| [LangChain tool](ai/langchain) | | |

---

## Common patterns

**Clean a list:** verify each address, keep `ok`, drop `ko`, review `mb` by hand or by risk tolerance.

**Validate at signup:** verify on form submit, block `ko` in real time so bad addresses never enter your database.

**Enrich before outreach:** combine our [email finder](https://mailtester.ninja/email-finder/) to build the address and the verifier to confirm it before you send.

## A note on privacy

MailTester Ninja verifies in real time and stores nothing. Addresses are processed in memory to return a verdict and are never saved, so there is nothing to leak and nothing to resell. Verification without a database.

## License

MIT, see [LICENSE](LICENSE). Use these examples freely in your own projects.

---

Built by [MailTester Ninja](https://mailtester.ninja). Questions? https://mailtester.ninja/contact/
