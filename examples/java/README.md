# Verify emails in Java

Verify email addresses from Java 11+ with the built in HTTP client. No dependencies.

## Run

```bash
export MAILTESTER_KEY=your_key
java MailTester.java      # single-file source launch, Java 11+
```

## Verify one address

```java
String json = verify("info@apple.com", System.getenv("MAILTESTER_KEY"));
// branch on the "code" field: "ok" valid, "ko" invalid, "mb" uncertain
```

[`MailTester.java`](MailTester.java) keeps zero dependencies with a tiny field extractor. **For production, parse the JSON with Jackson or Gson** instead of the regex helper.

## Rate limits

Pro = 11 req/10s, Ultimate = 23 req/10s. The example sleeps 1s between calls.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
