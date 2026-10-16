# Verify emails in Python

Verify email addresses from Python. Needs only `requests`.

## Install

```bash
pip install requests
export MAILTESTER_KEY=your_key   # get one at https://mailtester.ninja/verify-emails-unlimited/
```

## Verify one address

```python
import os
from mailtester import verify

result = verify("info@apple.com", os.environ["MAILTESTER_KEY"])
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
for email, res in clean_list(emails, key, delay=1.0):   # delay respects the rate limit
    if res["code"] == "ok":
        print("keep", email)
```

[`mailtester.py`](mailtester.py) does all three: a single check, list cleaning, and a commented CSV cleaner you can switch on. Run it with:

```bash
python mailtester.py
```

## Rate limits

Keep `delay` at roughly `10 / your_rate` seconds. Pro = 11 req/10s (so delay ~1s), Ultimate = 23 req/10s (so delay ~0.45s). Multiply your plan quantity at checkout to go faster.

Docs: https://mailtester.ninja/api/
