"""
A LangChain tool that verifies an email with MailTester Ninja.

pip install langchain-core requests
export MAILTESTER_KEY=...   optional: without it the free tier is used (key=free, 10 checks a day).
                            Free token (50 a day): https://mailtester.ninja/free-email-verification-api/
                            Paid key: https://mailtester.ninja/verify-emails-unlimited/

Attach `verify_email_tool` to any LangChain agent. The agent decides when to
call it; it returns a short, honest verdict string.
"""
import os
import requests
from langchain_core.tools import tool

MT_KEY = os.environ.get("MAILTESTER_KEY", "free")

@tool
def verify_email_tool(email: str) -> str:
    """Verify whether an email address is valid and deliverable, in real time.
    Returns the verdict code (ok valid, ko invalid, mb uncertain) and a label."""
    r = requests.get(
        "https://happy.mailtester.ninja/ninja",
        params={"email": email, "key": MT_KEY},
        timeout=30,
    )
    if r.status_code == 429:
        # Free tier limit (one request every 30 s, daily quota): not a verdict.
        return f"free tier limit, no verdict: {r.json().get('message')}"
    r.raise_for_status()
    d = r.json()
    return f"{d.get('code')} ({d.get('message')}) for {d.get('email')}"

if __name__ == "__main__":
    # Call the tool directly (no agent) to check it works.
    print(verify_email_tool.invoke({"email": "info@apple.com"}))
