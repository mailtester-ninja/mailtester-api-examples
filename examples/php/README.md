# Verify emails in PHP

Verify email addresses from PHP. Plain cURL, drops into any project or framework.

## Run

```bash
export MAILTESTER_KEY=your_key   # https://mailtester.ninja/verify-emails-unlimited/
php mailtester.php
```

## Verify one address

```php
require 'mailtester.php';

$r = mailtester_verify('info@apple.com', getenv('MAILTESTER_KEY'));
echo $r['code'] . ' ' . $r['message'];   // ok Accepted
```

## Reading the verdict

```php
switch ($r['code']) {
    case 'ok': break; // valid and deliverable, safe to send
    case 'ko': break; // invalid, will bounce, drop it
    case 'mb': break; // uncertain (catch-all or unprobeable), decide by risk
}
```

## Validate at signup (Laravel, Symfony, plain PHP)

```php
if (!mailtester_is_deliverable($request->input('email'), getenv('MAILTESTER_KEY'))) {
    // reject the form, the address will bounce
}
```

## Clean a list

```php
$results = mailtester_clean_list($emails, $key, 1.0); // delay seconds respects the rate limit
$keep = array_keys(array_filter($results, fn($r) => ($r['code'] ?? '') === 'ok'));
```

[`mailtester.php`](mailtester.php) holds `mailtester_verify`, `mailtester_is_deliverable` and `mailtester_clean_list`. Drop it in, or paste just the function you need.

## Rate limits

`$delay` ~= `10 / your_rate` seconds. Pro = 11 req/10s (~1.0s), Ultimate = 23 req/10s (~0.45s).

Docs: https://mailtester.ninja/api/
