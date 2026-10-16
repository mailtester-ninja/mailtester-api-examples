"""
MailTester Ninja, email verification in Python.

Verify one address or clean a whole list, over the real time API.
No dependencies beyond `requests`:  pip install requests

Get a key: https://mailtester.ninja/verify-emails-unlimited/
Docs:      https://mailtester.ninja/api/
"""

import os
import time
import csv
from urllib.parse import quote

import requests

ENDPOINT = "https://happy.mailtester.ninja/ninja"


def verify(email: str, key: str, timeout: int = 30) -> dict:
    """Verify a single email address. Returns the parsed API response.

    The useful field is `code`:
      "ok" -> valid and deliverable
      "ko" -> invalid, will bounce
      "mb" -> uncertain (catch-all, or the server could not be probed)
    `message` is a human readable label for the verdict.
    """
    resp = requests.get(
        ENDPOINT,
        params={"email": email, "key": key},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def is_deliverable(email: str, key: str) -> bool:
    """Convenience helper: True only when the address is clearly valid."""
    return verify(email, key).get("code") == "ok"


def clean_list(emails, key, delay: float = 1.0):
    """Verify a list of addresses, yielding (email, result) tuples.

    `delay` seconds between calls keeps you within the rate limit
    (Pro = 11 / 10s, Ultimate = 23 / 10s). Tune it to your plan.
    """
    for email in emails:
        email = email.strip()
        if not email:
            continue
        try:
            yield email, verify(email, key)
        except requests.RequestException as exc:
            yield email, {"code": "error", "message": str(exc)}
        time.sleep(delay)


if __name__ == "__main__":
    key = os.environ.get("MAILTESTER_KEY")
    if not key:
        raise SystemExit(
            "Set MAILTESTER_KEY. Get one at "
            "https://mailtester.ninja/verify-emails-unlimited/"
        )

    # 1) Verify one address
    result = verify("info@apple.com", key)
    print(f"{result['email']}: {result['code']} ({result['message']})")

    # 2) Clean a list and keep only deliverable addresses
    sample = ["info@apple.com", "test@gmail.com", "someone@example.com"]
    kept = []
    for email, res in clean_list(sample, key, delay=1.0):
        verdict = res.get("code")
        label = res.get("message", "")
        print(f"  {email:<30} {verdict:<6} {label}")
        if verdict == "ok":
            kept.append(email)
    print(f"\nDeliverable: {kept}")

    # 3) Clean a CSV (expects a column named 'email'), writes clean.csv
    #    Uncomment to run against your own file.
    # with open("contacts.csv") as fin, open("clean.csv", "w", newline="") as fout:
    #     reader = csv.DictReader(fin)
    #     writer = csv.writer(fout)
    #     writer.writerow(["email", "code", "message"])
    #     for row in reader:
    #         res = verify(row["email"], key)
    #         writer.writerow([row["email"], res.get("code"), res.get("message")])
    #         time.sleep(1.0)
