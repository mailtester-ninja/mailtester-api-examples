<?php
/**
 * MailTester Ninja, email verification in PHP.
 *
 * Plain PHP with cURL, no dependencies, no framework.
 * Get a key: https://mailtester.ninja/verify-emails-unlimited/
 * Docs:      https://mailtester.ninja/api/
 */

const MAILTESTER_ENDPOINT = 'https://happy.mailtester.ninja/ninja';

/**
 * Verify a single email address. Returns the decoded API response as an array.
 * The useful key is 'code': "ok" valid, "ko" invalid, "mb" uncertain.
 *
 * @throws RuntimeException on transport or HTTP error.
 */
function mailtester_verify(string $email, string $key, int $timeout = 30): array
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
function mailtester_is_deliverable(string $email, string $key): bool
{
    return (mailtester_verify($email, $key)['code'] ?? '') === 'ok';
}

/**
 * Verify a list. Returns [email => result]. $delay seconds between calls
 * keeps you within the rate limit (Pro 11/10s, Ultimate 23/10s).
 */
function mailtester_clean_list(array $emails, string $key, float $delay = 1.0): array
{
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

// Run directly:  MAILTESTER_KEY=xxx php mailtester.php
if (PHP_SAPI === 'cli' && isset($argv) && realpath($argv[0]) === __FILE__) {
    $key = getenv('MAILTESTER_KEY');
    if (!$key) {
        fwrite(STDERR, "Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/\n");
        exit(1);
    }

    // 1) one address
    $one = mailtester_verify('info@apple.com', $key);
    printf("%s: %s (%s)\n", $one['email'], $one['code'], $one['message']);

    // 2) clean a list
    $sample = ['info@apple.com', 'test@gmail.com', 'someone@example.com'];
    $kept = [];
    foreach (mailtester_clean_list($sample, $key, 1.0) as $email => $res) {
        printf("  %-30s %-6s %s\n", $email, $res['code'] ?? '?', $res['message'] ?? '');
        if (($res['code'] ?? '') === 'ok') {
            $kept[] = $email;
        }
    }
    echo "\nDeliverable: " . implode(', ', $kept) . "\n";
}
