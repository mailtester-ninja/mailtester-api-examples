# Verify emails in Ruby

Verify email addresses from Ruby using net/http. No gems required.

## Run

```bash
export MAILTESTER_KEY=your_key   # optional, see Keys below
ruby mailtester.rb
```

## Verify one address

```ruby
r = verify("info@apple.com", ENV.fetch("MAILTESTER_KEY", "free"))
# r["code"]: "ok" valid, "ko" invalid, "mb" uncertain ; r["message"] is the label
```

[`mailtester.rb`](mailtester.rb) has `verify` and `deliverable?` helpers and runs on its own.

## Keys

- **No key:** leave `MAILTESTER_KEY` unset and the example uses the free tier (`key=free`): 10 checks a day per IP, one request every 30 seconds.
- **Free token:** 50 checks a day, one request every 30 seconds, no card: https://mailtester.ninja/free-email-verification-api/
- **Paid key:** full speed, from 100,000 checks a day: https://mailtester.ninja/verify-emails-unlimited/

On the free tier the API answers HTTP 429 when you call too fast or reach the daily limit. That answer is not a verdict: its `message` says how long to wait, and the example reports it as an error.

## Rate limits

Free tier and free tokens: one request every 30 seconds, the example waits automatically. Pro = 11 req/10s, Ultimate = 23 req/10s. On a paid key the example sleeps 1s between calls.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
