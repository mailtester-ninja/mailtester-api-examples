# Verify emails in Python

Verify email addresses from Python. Needs only `requests`.

## Install

```bash
pip install requests
export MAILTESTER_KEY=your_key   # optional, see Keys below
```

## Verify one address

```python
import os
from mailtester import verify

result = verify("info@apple.com", os.environ.get("MAILTESTER_KEY", "free"))
print(result["code"], result["message"])   # ok Accepted
```

## Reading the verdict

```python
code = result["code"]
if code == "ok":
    ...  # valid and deliverable, safe to send
elif code == "ko":
    ...  # invalid, will bounce, drop it
elif code == "mb":
    ...  # uncertain (catch-all or unprobeable), decide by risk
```

## Clean a list

```python
from mailtester import clean_list

emails = ["info@apple.com", "test@gmail.com", "someone@example.com"]
for email, res in clean_list(emails, key):   # waits 30 s on the free tier, 1 s on a paid key
    if res["code"] == "ok":
        print("keep", email)
```

[`mailtester.py`](mailtester.py) does all three: a single check, list cleaning, and a commented CSV cleaner you can switch on. Run it with:

```bash
python mailtester.py
```

## Keys

- **No key:** leave `MAILTESTER_KEY` unset and the example uses the free tier (`key=free`): 10 checks a day per IP, one request every 30 seconds.
- **Free token:** 50 checks a day, one request every 30 seconds, no card: https://mailtester.ninja/free-email-verification-api/
- **Paid key:** full speed, from 100,000 checks a day: https://mailtester.ninja/verify-emails-unlimited/

On the free tier the API answers HTTP 429 when you call too fast or reach the daily limit. That answer is not a verdict: its `message` says how long to wait, and the example reports it as an error.

## Rate limits

Free tier and free tokens: one request every 30 seconds, the example waits automatically. Keep `delay` at roughly `10 / your_rate` seconds. Pro = 11 req/10s (so delay ~1s), Ultimate = 23 req/10s (so delay ~0.45s). Multiply your plan quantity at checkout to go faster.

Docs: https://mailtester.ninja/api/
