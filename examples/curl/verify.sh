#!/usr/bin/env bash
# Verify one email with the MailTester Ninja API.
# Usage: ./verify.sh someone@example.com                    (free tier, key=free, 10 checks a day)
#        MAILTESTER_KEY=your_key ./verify.sh someone@example.com
# Free token (50 a day): https://mailtester.ninja/free-email-verification-api/
# Paid key (full speed):  https://mailtester.ninja/verify-emails-unlimited/
set -euo pipefail

EMAIL="${1:?Usage: ./verify.sh email@example.com}"
KEY="${MAILTESTER_KEY:-free}"

ENC=$(jq -rn --arg e "$EMAIL" '$e|@uri')
OUT=$(curl -s -w '\n%{http_code}' "https://happy.mailtester.ninja/ninja?email=${ENC}&key=${KEY}")
STATUS=$(echo "$OUT" | tail -n1)
RESP=$(echo "$OUT" | sed '$d')

if [ "$STATUS" = "429" ]; then
  # Free limit reached: this is not a verdict, the message says how long to wait.
  echo "$RESP" | jq -r '.message'
  exit 2
fi

echo "$RESP" | jq
CODE=$(echo "$RESP" | jq -r '.code')

case "$CODE" in
  ok) echo "-> valid, safe to send" ;;
  ko) echo "-> invalid, will bounce, drop it" ;;
  mb) echo "-> uncertain (catch-all or unprobeable), decide by risk" ;;
  *)  echo "-> unexpected response" ;;
esac
