---
search:
  exclude: true

title: ESI OpenAPI
type: resource
description: Rust client library for ESI based on the OpenAPI 3.1 spec, with pagination, caching, bulk requests and rate limiting.
maintainer:
  name: rafaga
  github: rafaga
---

# ESI OpenAPI

A Rust client library for EVE Online's ESI. It is a fork of [rfesi](https://github.com/Celeo/rfesi) (from 0.50.2) that moves from ESI's retired Swagger 2.0 spec to the OpenAPI 3.1 spec. Migrating from rfesi mostly means replacing `use rfesi::` with `use esi_openapi::`.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/rafaga/esi-openapi){ .esi-card-link }
- [:octicons-package-16: __crates.io__](https://crates.io/crates/esi-openapi){ .esi-card-link }
- [:octicons-book-16: __docs.rs__](https://docs.rs/esi-openapi){ .esi-card-link }

</div>

## Features

- Covers all 233 operations in the ESI OpenAPI spec (compatibility date 2026-08-18) through endpoint groups (`Esi::group_*()`), checked by a conformance test.
- Pagination helpers, including access to the `X-Pages` count.
- Optional response cache that revalidates with `ETag`/`Last-Modified` and honors `x-client-cache-ttl`.
- Automatic splitting of bulk requests that exceed the spec's maximum list size.
- Optional rate-limit policy that waits or fails instead of triggering `429` errors (off by default).
- Sends the `X-Compatibility-Date` header and handles `X-Ratelimit-*` and `Retry-After`.
- Reads scopes, roles and rate limits declared per operation, and reloads the spec only when stale.
- Language and tenant settings, and a dedicated error for resources ESI has tombstoned.
- Operations not yet wrapped can be called with `Esi::get_endpoint_for_op_id` and `Esi::query`.

## Usage

```sh
cargo add esi-openapi
```

The `random_state`, `validate_jwt` and `rustls-tls` features are enabled by default; disable the first two if you don't need them. See the [documentation on docs.rs](https://docs.rs/esi-openapi) for the API, and the repository's `CHANGELOG.md` for the mapping from rfesi's operation IDs.

## License

Dual-licensed under Apache-2.0 or MIT, at your option. The original rfesi copyright notices are retained.
