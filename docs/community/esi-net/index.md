---
search:
  exclude: true

title: ESI.NET
type: resource
description: A .NET client for EVE Online's ESI API with SSO/PKCE auth, transparent token refresh, and full endpoint coverage.
maintainer:
  name: Psianna Archeia
  github: seraphx2
---

# ESI.NET

A .NET wrapper for EVE Online's ESI API, multi-targeting `netstandard2.0`, `net8.0`, and `net10.0`. Handles the SSO/OAuth2 flow (including PKCE), transparently refreshes near-expired access tokens before a request goes out, and wraps every ESI endpoint behind a typed client registered via `IHttpClientFactory`.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/seraphx2/ESI.NET){ .esi-card-link }
- [:simple-nuget: __NuGet__](https://www.nuget.org/packages/ESI.NET){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.gg/SvdN39f){ .esi-card-link }

</div>

## Features

- Every ESI endpoint wrapped behind a typed `IEsiClient`, organized by category (`client.Character`, `client.Assets`, `client.Universe`, ...)
- SSO/OAuth2 authentication, including the PKCE flow for public (secretless) clients
- Transparent access-token refresh - a near-expired token is refreshed automatically before an authenticated call goes out, with a DI-friendly hook to persist the rotated refresh token
- Per-call options for cancellation, conditional requests (`ETag`/`If-None-Match`), and pagination
- Actively monitored against CCP's live API every day, so new endpoints and spec changes get caught - and shipped - fast, not months later
