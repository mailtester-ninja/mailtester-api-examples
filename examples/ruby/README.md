# Verify emails in Ruby

Verify email addresses from Ruby using net/http. No gems required.

## Run

```bash
export MAILTESTER_KEY=your_key
ruby mailtester.rb
```

## Verify one address

```ruby
r = verify("info@apple.com", ENV["MAILTESTER_KEY"])
# r["code"]: "ok" valid, "ko" invalid, "mb" uncertain ; r["message"] is the label
```

[`mailtester.rb`](mailtester.rb) has `verify` and `deliverable?` helpers and runs on its own.

## Rate limits

Pro = 11 req/10s, Ultimate = 23 req/10s. The example sleeps 1s between calls.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
