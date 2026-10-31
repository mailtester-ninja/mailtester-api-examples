# Verify emails in Node.js

Verify email addresses from Node. Uses the built in `fetch` (Node 18+), so there is nothing to install.

## Run

```bash
export MAILTESTER_KEY=your_key   # optional, see Keys below
node mailtester.js
```

## Verify one address

```js
const { verify } = require('./mailtester');

const r = await verify('info@apple.com', process.env.MAILTESTER_KEY || 'free');
console.log(r.code, r.message);   // ok Accepted
```

## Reading the verdict

```js
switch (r.code) {
  case 'ok': break; // valid and deliverable, safe to send
  case 'ko': break; // invalid, will bounce, drop it
  case 'mb': break; // uncertain (catch-all or unprobeable), decide by risk
}
```

## Clean a list

```js
const { cleanList } = require('./mailtester');

const rows = await cleanList(emails, key); // waits 30 s on the free tier, 1 s on a paid key
const keep = rows.filter(r => r.result.code === 'ok').map(r => r.email);
```

[`mailtester.js`](mailtester.js) exports `verify`, `isDeliverable` and `cleanList`, and runs as is.

## Find a work email (paid key)

```js
const { find } = require('./mailtester');

const res = await find('Jane', 'Doe', 'example.com', process.env.MAILTESTER_KEY);
if (res.found) console.log(res.email);          // an address the mail server just accepted
else console.log(res.message, res.guess);       // e.g. Catch-All and the most likely address
console.log(res.permutations, 'formats tested'); // each one counts as a verification
```

`find()` throws on HTTP 429 (retry in a few seconds). Details: [Finder API](../../README.md#find-a-work-email-finder-api).

## ESM

Using `import`? Swap `require`/`module.exports` for `import`/`export`, the fetch call is identical.

## Keys

- **No key:** leave `MAILTESTER_KEY` unset and the example uses the free tier (`key=free`): 10 checks a day per IP, one request every 30 seconds.
- **Free token:** 50 checks a day, one request every 30 seconds, no card: https://mailtester.ninja/free-email-verification-api/
- **Paid key:** full speed, from 100,000 checks a day: https://mailtester.ninja/verify-emails-unlimited/

On the free tier the API answers HTTP 429 when you call too fast or reach the daily limit. That answer is not a verdict: its `message` says how long to wait, and the example reports it as an error.

## Rate limits

Free tier and free tokens: one request every 30 seconds, the example waits automatically. `delayMs` ~= `10000 / your_rate`. Pro = 11 req/10s (~1000ms), Ultimate = 23 req/10s (~450ms).

Docs: https://mailtester.ninja/api/
