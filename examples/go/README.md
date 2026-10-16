# Verify emails in Go

Verify email addresses from Go with the standard library. No modules to add.

## Run

```bash
export MAILTESTER_KEY=your_key
go run mailtester.go
```

## Verify one address

```go
r, err := Verify("info@apple.com", os.Getenv("MAILTESTER_KEY"))
// r.Code: "ok" valid, "ko" invalid, "mb" uncertain ; r.Message is the label
```

[`mailtester.go`](mailtester.go) has a typed `Result` and a `Verify` function. Copy `Verify` into your package as is.

## Rate limits

Pro = 11 req/10s, Ultimate = 23 req/10s. The example sleeps 1s between calls; tune to your plan.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
