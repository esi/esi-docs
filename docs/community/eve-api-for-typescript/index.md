---
search:
  exclude: true

title: EVE API for TypeScript
type: resource
description: Typed, validated TypeScript client for ESI with full spec coverage, spec-driven caching and rate limiting, SSO with PKCE, multi-character support and offline SDE lookups.
maintainer:
  name: Leigh Griffin
  github: lgriffin
---

# ESI.ts

[![npm version](https://badge.fury.io/js/%40lgriffin%2Fesi.ts.svg)](https://www.npmjs.com/package/@lgriffin/esi.ts)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4%2B-blue)](https://www.typescriptlang.org/)
[![CI/CD Pipeline](https://github.com/lgriffin/ESI.ts/actions/workflows/ci.yml/badge.svg)](https://github.com/lgriffin/ESI.ts/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/lgriffin/ESI.ts/badge)](https://scorecard.dev/viewer/?uri=github.com/lgriffin/ESI.ts)

A TypeScript client for the [EVE Online ESI API](https://esi.evetech.net/), built as an engineered product rather than a generated wrapper. It covers every operation in the ESI OpenAPI specification. Every response is validated at runtime, and caching, rate limiting, retry and pagination follow the rules ESI actually enforces.

<div class="grid cards" markdown>

- [:octicons-book-16: __Documentation__](https://lgriffin.github.io/ESI.ts/){ .esi-card-link }
- [:octicons-mark-github-16: __GitHub__](https://github.com/lgriffin/ESI.ts){ .esi-card-link }
- [:simple-npm: __npm__](https://www.npmjs.com/package/@lgriffin/esi.ts){ .esi-card-link }

</div>

The [documentation site](https://lgriffin.github.io/ESI.ts/) has the full guides, a page for every runnable example, and the [API reference](https://lgriffin.github.io/ESI.ts/api/) generated from the TSDoc.

## Install

```bash
npm install @lgriffin/esi.ts
```

Version 11 needs Node.js 22.12 or later; the 10.x line supports Node 18 and 20. TypeScript projects need TypeScript 5.4 or later, under `node16`, `nodenext` or `bundler` module resolution. The package ships as both ES module and CommonJS. [What 11.0 changes](https://lgriffin.github.io/ESI.ts/guide/usage#9-what-1100-changes) covers the upgrade from 10.x.

## Quick start

```typescript
import { EsiClient } from '@lgriffin/esi.ts';

const client = new EsiClient({ userAgent: 'my-app/1.0 (you@example.com)' });
try {
  const status = await client.status.getStatus();
  console.log(`${status.players} pilots online`);
} finally {
  client.shutdown();
}
```

Public data needs no token. For character data, pass an EVE SSO access token, or set `ESI_ACCESS_TOKEN`, and the client attaches it only to the calls that declare a scope:

```typescript
const character = await client.characters.getCharacterPublicInfo(characterId);
const prices = await client.market.getMarketPrices();

const authed = new EsiClient({ accessToken: token });
const wallet = await authed.wallet.getCharacterWallet(characterId);
```

## Multiple characters

An application that acts for many characters has one relationship with ESI, so `@lgriffin/esi.ts/client` builds one runtime and a view per identity. The views share the rate limiter, the error budget and the ETag cache; each identity's authenticated entries stay apart. `esi.public` is typed so that an authenticated call does not compile.

```typescript
import { createEsi } from '@lgriffin/esi.ts/client';

const esi = createEsi({ userAgent: 'my-app/1.0 (you@example.com)' });
const status = await esi.public.status.get();
const wallet = await esi
  .as(tokens.identity(characterId))
  .character(characterId)
  .wallet.get();
```

[Many characters](https://lgriffin.github.io/ESI.ts/guide/multi-character) covers identities (`EsiTokenManager`, a raw token, a `TokenProvider`) and what the views share.

## Testing your application without ESI

`createMockTransport()` from `@lgriffin/esi.ts/testing` answers requests from a table of routes and records what your code sent. Everything between your call and the transport is the real pipeline:

```typescript
import { createEsi, identityFromToken } from '@lgriffin/esi.ts/client';
import { createMockTransport } from '@lgriffin/esi.ts/testing';

const transport = createMockTransport().respond({
  method: 'GET',
  path: '/characters/{character_id}/wallet',
  body: 1234567.89,
});
const esi = createEsi({
  userAgent: 'my-app/1.0 (you@example.com)',
  transport,
});
try {
  const view = esi.as(identityFromToken('an-access-token'));
  const wallet = await view.character(2114794365).wallet.get();
  console.log(wallet); // 1234567.89
  console.log(transport.sent[0]?.headers['authorization']); // Bearer an-access-token
} finally {
  esi.shutdown();
}
```

## Features

| Capability              | What ESI.ts does                                                                                                                                                                                                             |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Full coverage**       | 39 domain clients covering all 233 operations in the ESI specification at compatibility date 2026-08-18, plus the specification documents themselves. The build fails if one is missing.                                       |
| **Runtime validation**  | Every GET response is checked against a hand-written Zod schema. Unknown fields pass through, so an additive change from CCP never breaks you. A changed shape throws `EsiValidationError` instead of corrupting your data. |
| **Caching**             | A GET inside ESI's cache window makes no HTTP call. Older entries are revalidated with ETags, and a 5xx serves the stale copy. A write invalidates the reads it affects. Keys are hashed per token.                          |
| **Rate limiting**       | One bucket per ESI rate-limit group, generated from the spec. The limiter learns from ESI's headers and honours `Retry-After`. A 420 or 429 blocks only its own group.                                                      |
| **Resilience**          | Exponential backoff with jitter, a single coalesced token refresh on 401, deduplication of identical in-flight GETs, and an opt-in circuit breaker. Each one is an interface you can replace.                                |
| **Pagination**          | Offset and cursor paging. `stream*` yields one validated page at a time, and `fetchAll*` fetches pages concurrently. `batch` and `batchPost` handle fan-out.                                                                 |
| **Authentication**      | EVE SSO with PKCE, and a token manager that handles storage, proactive refresh, rotation, revocation and bulk refresh for many characters.                                                                                   |
| **Static data**         | `@lgriffin/esi.ts/sde` answers offline queries over CCP's Static Data Export: typed lookups with no database.                                                                                                                |
| **Correct wire format** | Where the specification is wrong about how ESI reads a request, the definitions follow what ESI actually does, confirmed by live validation.                                                                                 |

The project is run to a written [engineering charter](https://lgriffin.github.io/ESI.ts/guide/charter): types, cache TTLs, rate-limit groups and scopes are generated from the OpenAPI spec, behaviour is specified as EARS requirements verified by BDD scenarios, and releases carry npm provenance, a signed SBOM and cosign signatures. [Testing](https://lgriffin.github.io/ESI.ts/guide/testing) has the current test, coverage and mutation figures.

## Entry points

| Import                        | What it holds                                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `@lgriffin/esi.ts`            | `EsiClient`, `EsiClientBuilder`, `EsiApiFactory`, domain clients, auth, errors, generated types and scopes |
| `@lgriffin/esi.ts/client`     | `createEsi`: one shared runtime, `esi.public` and `esi.as(identity)`                                        |
| `@lgriffin/esi.ts/schemas`    | The Zod response schemas                                                                                   |
| `@lgriffin/esi.ts/errors`     | Error classes and type guards, including the auth errors                                                   |
| `@lgriffin/esi.ts/testing`    | `createMockTransport` and `TestDataFactory` for your own tests                                             |
| `@lgriffin/esi.ts/sde`        | `SdeDataProvider` (YAML and ZIP) and `MemorySdeProvider`                                                   |
| `@lgriffin/esi.ts/sde/memory` | `MemorySdeProvider` alone, for browsers and bundles                                                        |

## Guides

- [Using the client](https://lgriffin.github.io/ESI.ts/guide/usage): construction, configuration, every domain client, batching
- [Authentication](https://lgriffin.github.io/ESI.ts/guide/authentication): tokens, refresh on 401, SSO with PKCE, the multi-character token manager
- [Pagination](https://lgriffin.github.io/ESI.ts/guide/pagination): offset and cursor paging, `stream*`, `fetchAll*`
- [Errors](https://lgriffin.github.io/ESI.ts/guide/errors): error classes, type guards, retryability
- [Static data (SDE)](https://lgriffin.github.io/ESI.ts/guide/sde): the offline Static Data Export module
- [Examples](https://lgriffin.github.io/ESI.ts/examples/): 58 runnable scripts, each with its source and the command that runs it

## License

GPL-3.0-or-later. EVE Online is the property of CCP hf.; this project is not affiliated with or endorsed by CCP.
