# Verify emails in Make (Integromat)

Check an address inside any Make scenario with the generic **HTTP > Make a request** module.

## Setup

1. Add an **HTTP > Make a request** module.
2. Fill it in:
   - **URL:** `https://happy.mailtester.ninja/ninja`
   - **Method:** `GET`
   - **Query String:** add two items
     - `email` = the field you are mapping
     - `key` = your key ([get one](https://mailtester.ninja/verify-emails-unlimited/))
   - **Parse response:** Yes (so Make reads the JSON for you).
3. Downstream modules can now map `code` and `message`.

## Branch on the verdict

Add a **Router** with filters on the HTTP module's `code`:
- `code` = `ok` route: valid, keep it.
- `code` = `ko` route: invalid, drop it.
- `code` = `mb` route: uncertain (catch-all), send to review.

## Rate limit

Over a list, add a **Sleep** module (about 1 second on Pro, 0.45s on Ultimate) or lower the scenario's cycle size. Pro = 11 req/10s, Ultimate = 23 req/10s.

## Keep the key out of the scenario

Store the key in a **data store** or a connection, not inline, so an exported blueprint never leaks it.

Docs: https://mailtester.ninja/api/
