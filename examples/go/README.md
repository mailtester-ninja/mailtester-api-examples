# Verify emails in Go

Verify email addresses from Go with the standard library. No modules to add.

## Run

```bash
export MAILTESTER_KEY=your_key   # optional, see Keys below
go run mailtester.go
```

## Verify one address

```go
key := os.Getenv("MAILTESTER_KEY")
if key == "" {
	key = "free" // free tier, no signup
}
r, err := Verify("info@apple.com", key)
// r.Code: "ok" valid, "ko" invalid, "mb" uncertain ; r.Message is the label
```

[`mailtester.go`](mailtester.go) has a typed `Result` and a `Verify` function. Copy `Verify` into your package as is.

## Find a work email (paid key)

The Finder API is the same kind of call: `GET https://happy.mailtester.ninja/find?first=Jane&last=Doe&domain=example.com&key=YOUR_KEY`, URL-encoded like the verification. Read `found`, `email`, `guess`, `code`, `message` and `permutations` from the JSON answer. Each format tested counts as one verification. Details: [Finder API](../../README.md#find-a-work-email-finder-api).

## Keys

- **No key:** leave `MAILTESTER_KEY` unset and the example uses the free tier (`key=free`): 10 checks a day per IP, one request every 30 seconds.
- **Free token:** 50 checks a day, one request every 30 seconds, no card: https://mailtester.ninja/free-email-verification-api/
- **Paid key:** full speed, from 100,000 checks a day: https://mailtester.ninja/verify-emails-unlimited/

On the free tier the API answers HTTP 429 when you call too fast or reach the daily limit. That answer is not a verdict: its `message` says how long to wait, and the example reports it as an error.

## Rate limits

Free tier and free tokens: one request every 30 seconds, the example waits automatically. Pro = 11 req/10s, Ultimate = 23 req/10s. On a paid key the example sleeps 1s between calls; tune to your plan.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
