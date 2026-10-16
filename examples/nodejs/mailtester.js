/**
 * MailTester Ninja, email verification in Node.js.
 *
 * Uses the built in fetch (Node 18+), no dependencies.
 * Get a key: https://mailtester.ninja/verify-emails-unlimited/
 * Docs:      https://mailtester.ninja/api/
 */

const ENDPOINT = 'https://happy.mailtester.ninja/ninja';

/**
 * Verify a single email address. Resolves to the parsed API response.
 * The useful field is `code`: "ok" valid, "ko" invalid, "mb" uncertain.
 */
async function verify(email, key) {
  const url = `${ENDPOINT}?email=${encodeURIComponent(email)}&key=${encodeURIComponent(key)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/** True only when the address is clearly valid and deliverable. */
async function isDeliverable(email, key) {
  const r = await verify(email, key);
  return r.code === 'ok';
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * Verify a list, respecting the rate limit.
 * delayMs between calls: ~1000 on Pro, ~450 on Ultimate.
 */
async function cleanList(emails, key, delayMs = 1000) {
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

// Run directly:  MAILTESTER_KEY=xxx node mailtester.js
if (require.main === module) {
  (async () => {
    const key = process.env.MAILTESTER_KEY;
    if (!key) {
      console.error('Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/');
      process.exit(1);
    }

    // 1) one address
    const one = await verify('info@apple.com', key);
    console.log(`${one.email}: ${one.code} (${one.message})`);

    // 2) clean a list
    const sample = ['info@apple.com', 'test@gmail.com', 'someone@example.com'];
    const rows = await cleanList(sample, key, 1000);
    const kept = [];
    for (const { email, result } of rows) {
      console.log(`  ${email.padEnd(30)} ${String(result.code).padEnd(6)} ${result.message || ''}`);
      if (result.code === 'ok') kept.push(email);
    }
    console.log('\nDeliverable:', kept);
  })();
}

module.exports = { verify, isDeliverable, cleanList };
