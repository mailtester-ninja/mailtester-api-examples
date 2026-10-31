/**
 * MailTester Ninja, email verification in Node.js, and the Finder API
 * (work email from a name and a company domain, paid key).
 *
 * Uses the built in fetch (Node 18+), no dependencies.
 * Keys:
 *   none set    -> free tier (key=free, 10 checks a day, one request every 30 s)
 *   free token  -> 50 checks a day: https://mailtester.ninja/free-email-verification-api/
 *   paid key    -> full speed: https://mailtester.ninja/verify-emails-unlimited/
 * Docs: https://mailtester.ninja/api/
 */

const ENDPOINT = 'https://happy.mailtester.ninja/ninja';
const FIND_ENDPOINT = 'https://happy.mailtester.ninja/find';
const FREE_KEY = 'free';
const FREE_DELAY_MS = 30000;

/** True for the keyless free tier and for free tokens (mtf_...). */
const isFree = (key) => key === FREE_KEY || String(key).startsWith('mtf_');

/**
 * Verify a single email address. Resolves to the parsed API response.
 * The useful field is `code`: "ok" valid, "ko" invalid, "mb" uncertain.
 * Throws when a free limit is reached (HTTP 429): that answer is not a verdict.
 */
async function verify(email, key = FREE_KEY) {
  const url = `${ENDPOINT}?email=${encodeURIComponent(email)}&key=${encodeURIComponent(key)}`;
  const res = await fetch(url);
  if (res.status === 429) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.message || 'Free API limit reached (HTTP 429)');
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * Find a work email address from a first name, a last name and a company domain (paid key).
 * MailTester Ninja tests the most common formats one by one (first.last, flast, first,
 * firstlast, first_last, f.last) and returns the first address the mail server accepts.
 * Useful fields: found, email, guess (catch-all domains, not verified), code, message,
 * permutations (formats tested, each one counted as a verification) and reason.
 * Throws on HTTP 429 (the key is at its maximum rate: retry in a few seconds) and on
 * other errors (400 invalid parameters, 403 free key).
 */
async function find(first, last, domain, key) {
  const qs = new URLSearchParams({ first, last, domain, key });
  const res = await fetch(`${FIND_ENDPOINT}?${qs}`);
  const body = await res.json().catch(() => ({}));
  if (res.status === 429) throw new Error(body.reason || 'Rate limit reached (HTTP 429), retry in a few seconds');
  if (!res.ok) throw new Error(body.reason || body.message || `HTTP ${res.status}`);
  return body;
}

/** True only when the address is clearly valid and deliverable. */
async function isDeliverable(email, key = FREE_KEY) {
  const r = await verify(email, key);
  return r.code === 'ok';
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * Verify a list, respecting the rate limit.
 * delayMs between calls: 30000 on the free tier, ~1000 on Pro, ~450 on Ultimate.
 */
async function cleanList(emails, key, delayMs = isFree(key) ? FREE_DELAY_MS : 1000) {
  const out = [];
  for (const raw of emails) {
    const email = String(raw).trim();
    if (!email) continue;
    try {
      out.push({ email, result: await verify(email, key) });
    } catch (err) {
      out.push({ email, result: { code: 'error', message: err.message } });
    }
    await sleep(delayMs);
  }
  return out;
}

// Run directly:  node mailtester.js   (or MAILTESTER_KEY=your_key node mailtester.js)
if (require.main === module) {
  (async () => {
    const key = process.env.MAILTESTER_KEY || FREE_KEY;
    if (isFree(key)) {
      console.log('Free tier: one request every 30 s. Paid keys go full speed: https://mailtester.ninja/verify-emails-unlimited/\n');
    }

    // 1) one address
    const one = await verify('info@apple.com', key);
    console.log(`${one.email}: ${one.code} (${one.message})`);
    if (isFree(key)) await sleep(FREE_DELAY_MS);

    // 2) clean a list
    const sample = ['info@apple.com', 'test@gmail.com', 'someone@example.com'];
    const rows = await cleanList(sample, key);
    const kept = [];
    for (const { email, result } of rows) {
      console.log(`  ${email.padEnd(30)} ${String(result.code).padEnd(6)} ${result.message || ''}`);
      if (result.code === 'ok') kept.push(email);
    }
    console.log('\nDeliverable:', kept);

    // 3) find a work email (Finder API, paid key only)
    if (!isFree(key)) {
      const found = await find('Jane', 'Doe', 'example.com', key);
      console.log(`\nFind Jane Doe at example.com: ${found.email || found.message} (${found.permutations} formats tested)`);
    }
  })();
}

module.exports = { verify, find, isDeliverable, cleanList, isFree };
