#!/usr/bin/env bash
# Find a work email with the MailTester Ninja Finder API (paid key).
# Usage: MAILTESTER_KEY=your_key ./find.sh Jane Doe example.com
#        MAILTESTER_KEY=your_key ./find.sh Jean-Pierre "De La Tour" example.com
# Each address format tested counts as one verification, even when nothing is found.
# Paid key: https://mailtester.ninja/verify-emails-unlimited/
set -euo pipefail

FIRST="${1:?Usage: ./find.sh FIRST LAST DOMAIN}"
LAST="${2:?Usage: ./find.sh FIRST LAST DOMAIN}"
DOMAIN="${3:?Usage: ./find.sh FIRST LAST DOMAIN}"
KEY="${MAILTESTER_KEY:?Set MAILTESTER_KEY to your paid key}"

enc() { jq -rn --arg v "$1" '$v|@uri'; }
OUT=$(curl -s -w '\n%{http_code}' "https://happy.mailtester.ninja/find?first=$(enc "$FIRST")&last=$(enc "$LAST")&domain=$(enc "$DOMAIN")&key=$(enc "$KEY")")
STATUS=$(echo "$OUT" | tail -n1)
RESP=$(echo "$OUT" | sed '$d')

if [ "$STATUS" = "429" ]; then
  # The key is at its maximum rate: not a result, retry in a few seconds.
  echo "$RESP" | jq -r '.reason'
  exit 2
fi
if [ "$STATUS" != "200" ]; then
  # 400 invalid parameters, 403 free key: the Finder API needs a paid key.
  echo "$RESP" | jq -r '.reason // .message' 2>/dev/null || echo "$RESP"
  exit 1
fi

echo "$RESP" | jq '{found, email, format, confidence, guess, code, message, permutations, tested, reason}'

if [ "$(echo "$RESP" | jq -r '.found')" = "true" ]; then
  echo "-> found: $(echo "$RESP" | jq -r '.email') ($(echo "$RESP" | jq -r '.format'), confidence $(echo "$RESP" | jq -r '.confidence'))"
elif [ "$(echo "$RESP" | jq -r '.guess')" != "null" ]; then
  echo "-> not confirmed, most likely: $(echo "$RESP" | jq -r '.guess') ($(echo "$RESP" | jq -r '.message'))"
else
  echo "-> not found ($(echo "$RESP" | jq -r '.message'))"
fi
