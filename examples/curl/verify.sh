#!/usr/bin/env bash
# Verify one email with the MailTester Ninja API.
# Usage: MAILTESTER_KEY=your_key ./verify.sh someone@example.com
set -euo pipefail

EMAIL="${1:?Usage: MAILTESTER_KEY=xxx ./verify.sh email@example.com}"
KEY="${MAILTESTER_KEY:?Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/}"

ENC=$(jq -rn --arg e "$EMAIL" '$e|@uri')
RESP=$(curl -s "https://happy.mailtester.ninja/ninja?email=${ENC}&key=${KEY}")

echo "$RESP" | jq
CODE=$(echo "$RESP" | jq -r '.code')

case "$CODE" in
  ok) echo "-> valid, safe to send" ;;
  ko) echo "-> invalid, will bounce, drop it" ;;
  mb) echo "-> uncertain (catch-all or unprobeable), decide by risk" ;;
  *)  echo "-> unexpected response" ;;
esac
