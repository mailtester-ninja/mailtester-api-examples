# OpenAI tool calling

Expose a `verify_email` function to an OpenAI model so it can check an address mid conversation.

## Run

```bash
pip install openai requests
export OPENAI_API_KEY=...
export MAILTESTER_KEY=...        # optional: free tier (key=free) when unset
python verify_tool.py
```

## How it works

[`verify_tool.py`](verify_tool.py) declares one tool, `verify_email(email)`, and handles the call loop: the model asks to call it, your code hits the API and returns `{email, code, message}`, the model answers. Swap the model name for whichever one you use.

The function hands the model a trimmed result and nothing else, so the model reports the real verdict instead of guessing. Treat `mb` as uncertain, not valid.

Docs: https://mailtester.ninja/api/

**Keys.** Without `MAILTESTER_KEY` the tool uses the free tier (`key=free`, 10 checks a day per IP, one request every 30 seconds). A [free token](https://mailtester.ninja/free-email-verification-api/) gives 50 checks a day; a [paid key](https://mailtester.ninja/verify-emails-unlimited/) removes the wait. When a free limit is hit, the tool returns `code: "limit"` with the API message, so the model reports the limit instead of a verdict.
