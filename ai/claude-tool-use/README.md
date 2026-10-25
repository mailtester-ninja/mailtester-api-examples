# Claude tool use

Give Claude a `verify_email` tool so it can check deliverability while it works.

## Run

```bash
pip install anthropic requests
export ANTHROPIC_API_KEY=...
export MAILTESTER_KEY=...        # optional: free tier (key=free) when unset
python verify_tool.py
```

## How it works

[`verify_tool.py`](verify_tool.py) defines the tool with an `input_schema`, then runs the tool loop until Claude stops asking for a call. Each call returns `{email, code, message}`. Point `model` at your current Claude model.

Keep the guardrail in your prompt: report the returned verdict, never invent one, and treat `mb` (catch-all or unprobeable) as uncertain.

Docs: https://mailtester.ninja/api/

**Keys.** Without `MAILTESTER_KEY` the tool uses the free tier (`key=free`, 10 checks a day per IP, one request every 30 seconds). A [free token](https://mailtester.ninja/free-email-verification-api/) gives 50 checks a day; a [paid key](https://mailtester.ninja/verify-emails-unlimited/) removes the wait. When a free limit is hit, the tool returns `code: "limit"` with the API message, so the model reports the limit instead of a verdict.
