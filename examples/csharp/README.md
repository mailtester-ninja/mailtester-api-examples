# Verify emails in C#

Verify email addresses from .NET 6+ with `HttpClient` and `System.Text.Json`.

## Run

```bash
export MAILTESTER_KEY=your_key
dotnet run
```

(Create a project with `dotnet new console` and drop in [`Program.cs`](Program.cs).)

## Verify one address

```csharp
var r = await Verify("info@apple.com");
var code = r.GetProperty("code").GetString();   // "ok" valid, "ko" invalid, "mb" uncertain
```

## Rate limits

Pro = 11 req/10s, Ultimate = 23 req/10s. The example awaits 1s between calls.

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
