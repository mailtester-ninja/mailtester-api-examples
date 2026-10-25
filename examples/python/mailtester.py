"""
MailTester Ninja, email verification in Python.

Verify one address or clean a whole list, over the real time API.
No dependencies beyond `requests`:  pip install requests

Keys:
  - none set      -> the free tier is used (key=free, 10 checks a day, one request every 30 s)
  - free token    -> 50 checks a day, one request every 30 s: https://mailtester.ninja/free-email-verification-api/
  - paid key      -> full speed: https://mailtester.ninja/verify-emails-unlimited/
Docs: https://mailtester.ninja/api/
"""

import os
import time
import csv
from urllib.parse import quote

import requests

ENDPOINT = "https://happy.mailtester.ninja/ninja"
FREE_KEY = "free"          # no signup, 10 checks a day per IP
FREE_DELAY = 30.0          # free tier: one request every 30 seconds


class FreeLimitError(RuntimeError):
    """The free tier refused the call (HTTP 429): wait, or use a paid key."""


def is_free(key: str) -> bool:
    """True for the keyless free tier and for free tokens (mtf_...)."""
    return key == FREE_KEY or key.startswith("mtf_")


def verify(email: str, key: str = FREE_KEY, timeout: int = 30) -> dict:
    """Verify a single email address. Returns the parsed API response.

    The useful field is `code`:
      "ok" -> valid and deliverable
      "ko" -> invalid, will bounce
      "mb" -> uncertain (catch-all, or the server could not be probed)
    `message` is a human readable label for the verdict.

    Raises FreeLimitError when a free limit is reached (HTTP 429). That
    response is not a verdict: its message says how long to wait.
    """
    resp = requests.get(
        ENDPOINT,
        params={"email": email, "key": key},
        timeout=timeout,
    )
    if resp.status_code == 429:
        raise FreeLimitError(resp.json().get("message", "Free API limit reached"))
    resp.raise_for_status()
    return resp.json()


def is_deliverable(email: str, key: str = FREE_KEY) -> bool:
    """Convenience helper: True only when the address is clearly valid."""
    return verify(email, key).get("code") == "ok"


def clean_list(emails, key, delay: float = None):
    """Verify a list of addresses, yielding (email, result) tuples.

    `delay` seconds between calls keeps you within the rate limit. By default:
    30 s on the free tier, 1 s on a paid key (Pro = 11 / 10s, Ultimate = 23 / 10s).
    """
    if delay is None:
        delay = FREE_DELAY if is_free(key) else 1.0
    for email in emails:
        email = email.strip()
        if not email:
            continue
        try:
            yield email, verify(email, key)
        except (requests.RequestException, FreeLimitError) as exc:
            yield email, {"code": "error", "message": str(exc)}
        time.sleep(delay)


if __name__ == "__main__":
    key = os.environ.get("MAILTESTER_KEY", FREE_KEY)
    if is_free(key):
        print("Free tier: one request every 30 s. Paid keys go full speed: "
              "https://mailtester.ninja/verify-emails-unlimited/\n")

    # 1) Verify one address
    result = verify("info@apple.com", key)
    print(f"{result['email']}: {result['code']} ({result['message']})")
    if is_free(key):
        time.sleep(FREE_DELAY)

    # 2) Clean a list and keep only deliverable addresses
    sample = ["info@apple.com", "test@gmail.com", "someone@example.com"]
    kept = []
    for email, res in clean_list(sample, key):
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
    #         time.sleep(FREE_DELAY if is_free(key) else 1.0)
