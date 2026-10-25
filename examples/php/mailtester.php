<?php
/**
 * MailTester Ninja, email verification in PHP.
 *
 * Plain PHP with cURL, no dependencies, no framework.
 * Keys:
 *   none set    -> free tier (key=free, 10 checks a day, one request every 30 s)
 *   free token  -> 50 checks a day: https://mailtester.ninja/free-email-verification-api/
 *   paid key    -> full speed: https://mailtester.ninja/verify-emails-unlimited/
 * Docs: https://mailtester.ninja/api/
 */

const MAILTESTER_ENDPOINT = 'https://happy.mailtester.ninja/ninja';
const MAILTESTER_FREE_KEY = 'free';
const MAILTESTER_FREE_DELAY = 30.0;

/** True for the keyless free tier and for free tokens (mtf_...). */
function mailtester_is_free(string $key): bool
{
    return $key === MAILTESTER_FREE_KEY || str_starts_with($key, 'mtf_');
}

/**
 * Verify a single email address. Returns the decoded API response as an array.
 * The useful key is 'code': "ok" valid, "ko" invalid, "mb" uncertain.
 *
 * @throws RuntimeException on transport or HTTP error, and when a free limit is
 *         reached (HTTP 429): that answer is not a verdict, its message says how long to wait.
 */
function mailtester_verify(string $email, string $key = MAILTESTER_FREE_KEY, int $timeout = 30): array
{
    $url = MAILTESTER_ENDPOINT . '?' . http_build_query(['email' => $email, 'key' => $key]);

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => $timeout,
        CURLOPT_USERAGENT      => 'mailtester-php-example',
    ]);
    $body = curl_exec($ch);
    if ($body === false) {
        $err = curl_error($ch);
        curl_close($ch);
        throw new RuntimeException("Request failed: $err");
    }
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($status === 429) {
        $msg = json_decode($body, true)['message'] ?? 'Free API limit reached';
        throw new RuntimeException($msg);
    }
    if ($status < 200 || $status >= 300) {
        throw new RuntimeException("HTTP $status");
    }

    $data = json_decode($body, true);
    if (!is_array($data)) {
        throw new RuntimeException('Invalid JSON response');
    }
    return $data;
}

/** True only when the address is clearly valid and deliverable. */
function mailtester_is_deliverable(string $email, string $key = MAILTESTER_FREE_KEY): bool
{
    return (mailtester_verify($email, $key)['code'] ?? '') === 'ok';
}

/**
 * Verify a list. Returns [email => result]. $delay seconds between calls keeps you
 * within the rate limit: 30 s on the free tier, 1 s on a paid key (Pro 11/10s, Ultimate 23/10s).
 */
function mailtester_clean_list(array $emails, string $key, ?float $delay = null): array
{
    $delay = $delay ?? (mailtester_is_free($key) ? MAILTESTER_FREE_DELAY : 1.0);
    $out = [];
    foreach ($emails as $email) {
        $email = trim((string) $email);
        if ($email === '') {
            continue;
        }
        try {
            $out[$email] = mailtester_verify($email, $key);
        } catch (RuntimeException $e) {
            $out[$email] = ['code' => 'error', 'message' => $e->getMessage()];
        }
        usleep((int) ($delay * 1_000_000));
    }
    return $out;
}

// Run directly:  php mailtester.php   (or MAILTESTER_KEY=your_key php mailtester.php)
if (PHP_SAPI === 'cli' && isset($argv) && realpath($argv[0]) === __FILE__) {
    $key = getenv('MAILTESTER_KEY') ?: MAILTESTER_FREE_KEY;
    if (mailtester_is_free($key)) {
        echo "Free tier: one request every 30 s. Paid keys go full speed: https://mailtester.ninja/verify-emails-unlimited/\n\n";
    }

    // 1) one address
    $one = mailtester_verify('info@apple.com', $key);
    printf("%s: %s (%s)\n", $one['email'], $one['code'], $one['message']);
    if (mailtester_is_free($key)) {
        usleep((int) (MAILTESTER_FREE_DELAY * 1_000_000));
    }

    // 2) clean a list
    $sample = ['info@apple.com', 'test@gmail.com', 'someone@example.com'];
    $kept = [];
    foreach (mailtester_clean_list($sample, $key) as $email => $res) {
        printf("  %-30s %-6s %s\n", $email, $res['code'] ?? '?', $res['message'] ?? '');
        if (($res['code'] ?? '') === 'ok') {
            $kept[] = $email;
        }
    }
    echo "\nDeliverable: " . implode(', ', $kept) . "\n";
}
