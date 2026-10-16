"""
Give an OpenAI model a verify_email tool backed by MailTester Ninja.

pip install openai requests
export OPENAI_API_KEY=...        export MAILTESTER_KEY=...   (https://mailtester.ninja/verify-emails-unlimited/)
"""
import os, json, requests
from openai import OpenAI

client = OpenAI()
MT_KEY = os.environ["MAILTESTER_KEY"]

# The tool the model can call.
TOOLS = [{
    "type": "function",
    "function": {
        "name": "verify_email",
        "description": "Check whether an email address is valid and deliverable, in real time.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "The email address to verify."}
            },
            "required": ["email"],
        },
    },
}]

def verify_email(email: str) -> dict:
    r = requests.get("https://happy.mailtester.ninja/ninja",
                     params={"email": email, "key": MT_KEY}, timeout=30)
    r.raise_for_status()
    d = r.json()
    # Hand the model a compact, honest result.
    return {"email": d.get("email"), "code": d.get("code"), "message": d.get("message")}

def run(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
    msg = resp.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = verify_email(args["email"])
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })
        resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
        msg = resp.choices[0].message

    return msg.content

if __name__ == "__main__":
    print(run("Is info@apple.com a real, deliverable address? Answer VALID, INVALID or UNCERTAIN."))
