"""
Give Claude a verify_email tool backed by MailTester Ninja.

pip install anthropic requests
export ANTHROPIC_API_KEY=...     export MAILTESTER_KEY=...   (https://mailtester.ninja/verify-emails-unlimited/)
"""
import os, requests
import anthropic

client = anthropic.Anthropic()
MT_KEY = os.environ["MAILTESTER_KEY"]

TOOLS = [{
    "name": "verify_email",
    "description": "Check whether an email address is valid and deliverable, in real time.",
    "input_schema": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address to verify."}
        },
        "required": ["email"],
    },
}]

def verify_email(email: str) -> dict:
    r = requests.get("https://happy.mailtester.ninja/ninja",
                     params={"email": email, "key": MT_KEY}, timeout=30)
    r.raise_for_status()
    d = r.json()
    return {"email": d.get("email"), "code": d.get("code"), "message": d.get("message")}

def run(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    while True:
        resp = client.messages.create(
            model="claude-sonnet-4-5"  # set to your current Claude model, max_tokens=400, tools=TOOLS, messages=messages,
        )
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")

        messages.append({"role": "assistant", "content": resp.content})
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use" and block.name == "verify_email":
                result = verify_email(block.input["email"])
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    print(run("Is info@apple.com a real, deliverable address? Answer VALID, INVALID or UNCERTAIN."))
