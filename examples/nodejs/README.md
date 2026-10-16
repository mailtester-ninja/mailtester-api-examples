# Verify emails in Node.js

Verify email addresses from Node. Uses the built in `fetch` (Node 18+), so there is nothing to install.

## Run

```bash
export MAILTESTER_KEY=your_key   # https://mailtester.ninja/verify-emails-unlimited/
node mailtester.js
```

## Verify one address

```js
const { verify } = require('./mailtester');

const r = await verify('info@apple.com', process.env.MAILTESTER_KEY);
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

const rows = await cleanList(emails, key, 1000); // delayMs respects the rate limit
const keep = rows.filter(r => r.result.code === 'ok').map(r => r.email);
```

[`mailtester.js`](mailtester.js) exports `verify`, `isDeliverable` and `cleanList`, and runs as is.

## ESM

Using `import`? Swap `require`/`module.exports` for `import`/`export`, the fetch call is identical.

## Rate limits

`delayMs` ~= `10000 / your_rate`. Pro = 11 req/10s (~1000ms), Ultimate = 23 req/10s (~450ms).

Docs: https://mailtester.ninja/api/
