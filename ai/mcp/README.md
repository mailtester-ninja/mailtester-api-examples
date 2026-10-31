# MCP server

MailTester Ninja runs an official remote MCP server, so Claude, Cursor, VS Code or any MCP client can verify emails without writing a single tool definition. Point the client at the URL, pass your key, and the agent gets two tools.

| | |
|---|---|
| Endpoint | `https://mcp.mailtester.ninja/mcp` |
| Transport | Streamable HTTP |
| Auth | `X-API-Key: YOUR_KEY` header, or `Authorization: Bearer YOUR_KEY`, or `?key=YOUR_KEY` in the URL |
| Official MCP Registry | [`ninja.mailtester/email-verification`](https://registry.modelcontextprotocol.io/v0.1/servers/ninja.mailtester%2Femail-verification/versions/latest) |
| Setup guide | https://mailtester.ninja/integrations/mcp/ |

No key yet? A [free API token](https://mailtester.ninja/free-email-verification-api/) gives 50 checks a day (one request every 30 seconds). Paid keys (`sub_...`) lift the limits and unlock `find_email`.

## Tools

| Tool | Input | Returns |
|---|---|---|
| `verify_email` | `email` | `code` (`ok` valid, `ko` invalid, `mb` uncertain), `message` (Accepted, Rejected, Catch-All, No MX, Disposable...), `domain`, `mx` |
| `find_email` | `first_name`, `last_name`, `domain` | `found`, `email`, `format`, `confidence`, `guess`, `code`, `message`, `tried`, `tested`, `reason`. Calls the [Finder API](../../README.md#find-a-work-email-finder-api): the 6 most common formats are tested one by one until the mail server accepts one; on a catch-all domain, `guess` holds the most common format. Paid key only, each format tested counts as one check. |

No message is ever sent, and the server keeps no copy of the addresses it checks.

## Connect your client

### Claude Code

```bash
claude mcp add --transport http mailtester-ninja https://mcp.mailtester.ninja/mcp --header "X-API-Key: YOUR_KEY"
```

### Claude Desktop and claude.ai

Settings, Connectors, Add custom connector, then paste the URL with the key at the end:

```
https://mcp.mailtester.ninja/mcp?key=YOUR_KEY
```

### Cursor

Merge [`cursor.json`](cursor.json) into `~/.cursor/mcp.json`.

### VS Code (GitHub Copilot)

Copy [`vscode.json`](vscode.json) to `.vscode/mcp.json`. VS Code prompts for the key once and stores it as a secret.

### Anything else

Use the endpoint with the `X-API-Key` header. If the client only takes a URL, append `?key=YOUR_KEY`.

## Try it

- "Is jane.doe@example.com a real address?"
- "Here are 20 signups, tell me which ones will bounce."
- "What is John Smith's work email at example.com?"

The server instructs the agent to report the verdict it received and to treat `mb` as uncertain, never as valid.

Keep the key out of shared config files and screenshots: prefer the header, and your client's secret storage, over the `?key=` URL.
