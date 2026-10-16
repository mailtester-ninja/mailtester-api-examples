# Claude tool use

Give Claude a `verify_email` tool so it can check deliverability while it works.

## Run

```bash
pip install anthropic requests
export ANTHROPIC_API_KEY=...
export MAILTESTER_KEY=...        # https://mailtester.ninja/verify-emails-unlimited/
python verify_tool.py
```

## How it works

[`verify_tool.py`](verify_tool.py) defines the tool with an `input_schema`, then runs the tool loop until Claude stops asking for a call. Each call returns `{email, code, message}`. Point `model` at your current Claude model.

Keep the guardrail in your prompt: report the returned verdict, never invent one, and treat `mb` (catch-all or unprobeable) as uncertain.

Docs: https://mailtester.ninja/api/
