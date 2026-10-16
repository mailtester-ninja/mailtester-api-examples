# Verify emails in Zapier

No MailTester Ninja app is needed. Use the built in **Webhooks by Zapier** action (GET), available on paid Zapier plans.

## Setup

1. Add an action step, pick **Webhooks by Zapier > GET**.
2. Configure:
   - **URL:** `https://happy.mailtester.ninja/ninja`
   - **Query String Params:**
     - `email` = the email from a previous step
     - `key` = your key ([get one](https://mailtester.ninja/verify-emails-unlimited/))
3. Zapier parses the JSON. Later steps can use `code` and `message`.

## Act on the result

Add a **Filter by Zapier** step, "Only continue if" `code` **(Text) Exactly matches** `ok`, to let only deliverable addresses through. Or use **Paths** to handle `ok`, `ko` and `mb` differently.

## One at a time

Zapier runs per record, which fits the rate limit naturally. For large backfills, throttle the trigger or add a **Delay** step so you stay under 11 req/10s (Pro) or 23 req/10s (Ultimate).

Docs: https://mailtester.ninja/api/
