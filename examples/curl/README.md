# Verify an email with cURL

The API is a single GET request, so cURL is all you need to try it.

## Verify one address

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

```bash
#!/usr/bin/env bash
# verify.sh , usage: MAILTESTER_KEY=xxx ./verify.sh someone@example.com
set -euo pipefail
EMAIL="$1"
KEY="${MAILTESTER_KEY:?Set MAILTESTER_KEY, get one at https://mailtester.ninja/verify-emails-unlimited/}"

# URL encode the email with jq
ENC=$(jq -rn --arg e "$EMAIL" '$e|@uri')

CODE=$(curl -s "https://happy.mailtester.ninja/ninja?email=${ENC}&key=${KEY}" | jq -r '.code')

case "$CODE" in
  ok) echo "valid, safe to send" ;;
  ko) echo "invalid, will bounce, drop it" ;;
  mb) echo "uncertain (catch-all or unprobeable), decide by risk" ;;
  *)  echo "unexpected response: $CODE" ;;
esac
```

See [`verify.sh`](verify.sh) in this folder.

## Notes

- URL encode the `email` value (the `+` and some characters matter).
- Remove the `{` and `}` from your key.
- Respect the rate limit (11 req / 10s on Pro, 23 on Ultimate). For a list, add `sleep` between calls.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
