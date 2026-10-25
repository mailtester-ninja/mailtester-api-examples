# LangChain tool

A ready made LangChain tool that verifies an email address.

## Run

```bash
pip install langchain-core requests
export MAILTESTER_KEY=...        # optional: free tier (key=free) when unset
python mailtester_tool.py        # calls the tool directly to check it works
```

## Use it in an agent

```python
from mailtester_tool import verify_email_tool

# add verify_email_tool to your agent's tool list
agent = create_react_agent(llm, tools=[verify_email_tool])
```

[`mailtester_tool.py`](mailtester_tool.py) wraps the GET call with the `@tool` decorator and returns a short verdict string (`ok`, `ko` or `mb` plus the label). The agent decides when to call it.

Docs: https://mailtester.ninja/api/

**Keys.** Without `MAILTESTER_KEY` the tool uses the free tier (`key=free`, 10 checks a day per IP, one request every 30 seconds). A [free token](https://mailtester.ninja/free-email-verification-api/) gives 50 checks a day; a [paid key](https://mailtester.ninja/verify-emails-unlimited/) removes the wait. When a free limit is hit, the tool returns `code: "limit"` with the API message, so the model reports the limit instead of a verdict.
