# Prompts for AI agents

Give an AI agent the ability to verify an email with MailTester Ninja. These are copy and paste prompts and a tool definition you can drop into ChatGPT, Claude, or any agent framework.

The agent calls one endpoint:

```
GET https://happy.mailtester.ninja/ninja?email=<EMAIL>&key=<YOUR_KEY>
```

and reads `code` (`ok` valid, `ko` invalid, `mb` uncertain) plus `message`.

---

## 1. System prompt (give the agent the skill)

```
You can verify whether an email address is real and deliverable using the
MailTester Ninja API. To verify an address, make a GET request to:
  https://happy.mailtester.ninja/ninja?email=<EMAIL>&key=<YOUR_KEY>
URL encode the email. Read the JSON field "code":
  - "ok": the address is valid and deliverable.
  - "ko": the address is invalid and will bounce.
  - "mb": uncertain. The domain is catch-all or could not be probed; do not
    claim it is valid.
Report the verdict using the "message" field, and never invent a result:
only state what the API returned.
```

## 2. One shot prompt (inside a tool enabled chat)

```
Verify this email with MailTester Ninja and tell me if it is safe to send to:
<EMAIL>
Call the endpoint, then answer in one line: VALID, INVALID, or UNCERTAIN,
followed by the message.
```

## 3. Bulk clean prompt

```
Here is a list of emails. Verify each one with MailTester Ninja, then return
a table with columns: email, code, message, keep (yes if code is ok, no
otherwise). Verify them one at a time and respect the rate limit.
<PASTE LIST>
```

## Guardrails worth keeping

- Tell the agent to **report, not guess**. The value of the tool is an honest verdict; an agent that fabricates "valid" defeats the purpose.
- Treat `mb` as **uncertain**, not valid. Catch-all domains accept everything.
- Keep the key in an environment variable or the framework's secret store, never in the prompt text you log.

See the framework specific examples:
- [OpenAI tool calling](../openai-tool-calling)
- [Claude tool use](../claude-tool-use)
- [LangChain tool](../langchain)

Docs: https://mailtester.ninja/api/ · Get a key: https://mailtester.ninja/verify-emails-unlimited/
