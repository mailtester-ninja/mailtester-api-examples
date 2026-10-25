# Verify an email with cURL

The API is a single GET request, so cURL is all you need to try it.

## Verify one address

Try it right now, no signup: `key=free` gives 10 checks a day per IP, one request every 30 seconds.

```bash
curl "https://happy.mailtester.ninja/ninja?email=info@apple.com&key=free"
```

With a free token (50 checks a day, [get one](https://mailtester.ninja/free-email-verification-api/)) or a paid key ([plans](https://mailtester.ninja/verify-emails-unlimited/)), put it in `key` instead:

```bash
curl "https://happy.mailtester.ninja/ninja?email=info@apple.com&key=YOUR_KEY"
```

```json
{"email":"info@apple.com","user":"Info","domain":"apple.com","mx":"mx-in.g.apple.com","code":"ok","message":"Accepted","connections":1}
```

## Pretty print with jq

```bash
curl -s "https://happy.mailtester.ninja/ninja?email=info@apple.com&key=YOUR_KEY" | jq
```

## Act on the verdict in bash

[`verify.sh`](verify.sh) verifies one address and prints what to do. It uses `MAILTESTER_KEY` when set, the free tier otherwise:

```bash
./verify.sh someone@example.com                      # free tier
MAILTESTER_KEY=your_key ./verify.sh someone@example.com
```

On the free tier, a call made too soon or past the daily limit gets HTTP 429. The script prints the API message (how long to wait) and exits with code 2, instead of showing a verdict.

See [`verify.sh`](verify.sh) in this folder.

## Notes

- URL encode the `email` value (the `+` and some characters matter).
- Remove the `{` and `}` from your key.
- Respect the rate limit (11 req / 10s on Pro, 23 on Ultimate). For a list, add `sleep` between calls.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
