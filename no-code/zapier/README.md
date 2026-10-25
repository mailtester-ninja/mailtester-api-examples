# Verify emails in Zapier

No MailTester Ninja app is needed. Use the built in **Webhooks by Zapier** action (GET), available on paid Zapier plans.

## Setup

1. Add an action step, pick **Webhooks by Zapier > GET**.
2. Configure:
   - **URL:** `https://happy.mailtester.ninja/ninja`
   - **Query String Params:**
     - `email` = the email from a previous step
     - `key` = your [paid key](https://mailtester.ninja/verify-emails-unlimited/), or a [free token](https://mailtester.ninja/free-email-verification-api/) to try it (50 checks a day, one request every 30 seconds)
3. Zapier parses the JSON. Later steps can use `code` and `message`.

## Act on the result

Add a **Filter by Zapier** step, "Only continue if" `code` **(Text) Exactly matches** `ok`, to let only deliverable addresses through. Or use **Paths** to handle `ok`, `ko` and `mb` differently.

## One at a time

Zapier runs per record, which fits the rate limit naturally. For large backfills, throttle the trigger or add a **Delay** step so you stay under 11 req/10s (Pro) or 23 req/10s (Ultimate).

## Free tier

Avoid `key=free` in Zapier: its servers share their IP addresses with all its users, and the keyless tier is counted per IP. With a free token, space calls by 30 seconds: on the free tier the API answers HTTP 429 when you call too fast or reach the daily limit, and that answer is not a verdict. A paid key removes the wait.

Docs: https://mailtester.ninja/api/
