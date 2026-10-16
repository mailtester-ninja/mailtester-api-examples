# LangChain tool

A ready made LangChain tool that verifies an email address.

## Run

```bash
pip install langchain-core requests
export MAILTESTER_KEY=...        # https://mailtester.ninja/verify-emails-unlimited/
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
