---
title: Getting Started
---

# Getting Started with EVE Third-Party Development

Build your first EVE Online application — from zero to authenticated API calls
in under 30 minutes.

## What You'll Build

By the end of this guide, you will:

1. Make your first public ESI call (server status)
2. Authenticate a character through EVE SSO
3. Read your character's in-game location
4. Handle token refresh so your app stays authenticated

## Prerequisites

- An EVE Online account (Alpha or Omega)
- **Python 3.9+** with `requests` installed, **or** **Node.js 18+** (TypeScript)
- A text editor and terminal

Install the Python dependency if using Python:

```bash
pip install requests
```

No extra packages needed for TypeScript — Node.js 18+ includes `fetch` natively.

## How EVE Third-Party Development Works

EVE provides two main services for developers:

- **ESI (EVE Swagger Interface)** — the REST API for all game data
- **EVE SSO (Single Sign-On)** — OAuth2 authentication for character-specific data

Here's the high-level flow from registration to a working app:

``` mermaid
graph LR
    A[Register App] --> B[Public API Calls]
    B --> C[SSO Login]
    C --> D[Authenticated Calls]
    D --> E[Token Refresh]
    E --> F[Build Your App]
```

**Public endpoints** (market data, universe info, server status) need no authentication.
**Character endpoints** (location, skills, wallet) require SSO tokens.

## Registering Your Application

Before making authenticated calls, register your application:

1. Go to [developers.eveonline.com](https://developers.eveonline.com/)
2. Log in with your EVE account
3. Click **Create New Application**
4. Fill in the form:
    - **Name**: Your application name (e.g., "My First EVE App")
    - **Description**: Brief description of your app
    - **Connection Type**: Choose **Authentication & API Access**
    - **Permissions**: Select the ESI scopes your app needs. For this guide, select
      `esi-location.read_location.v1`
    - **Callback URL**: `http://localhost:8089/callback`
5. Click **Create Application**
6. Note your **Client ID** and **Secret Key** — you'll need both

!!! warning

    Never commit your Client Secret to version control. Use environment variables
    or a configuration file excluded from git.

!!! tip

    The callback URL must match exactly between your registration and your code.
    For local development, `http://localhost:8089/callback` is a good default.

## Your First ESI Call

Let's start with an unauthenticated call to verify everything works. The
`/v2/status/` endpoint returns the current Tranquility server status — no
authentication needed.

--8<-- "snippets/getting-started/hello-esi.md"

Run it:

=== "Python"

    ```bash
    python hello-esi.py
    ```

=== "TypeScript"

    ```bash
    npx tsx hello-esi.ts
    ```

Expected output (values will vary):

```
Players online: 24531
Server version: 2431713
Started at:     2025-01-15T11:05:00Z
```

!!! note

    Always set a descriptive `User-Agent` header. ESI uses it to contact you if
    your application causes issues. Include your app name and a contact email.

## Understanding SSO Authentication

ESI uses **OAuth 2.0 Authorization Code** flow. Here's how it works:

``` mermaid
sequenceDiagram
    participant User as Player
    participant App as Your App
    participant SSO as EVE SSO
    participant ESI as ESI API

    App->>User: Open browser to SSO
    User->>SSO: Log in & authorize scopes
    SSO->>App: Redirect with authorization code
    App->>SSO: Exchange code for tokens
    SSO->>App: Access token + refresh token
    App->>ESI: API call with access token
    ESI->>App: Character data
```

Key concepts:

- **Authorization code** — Short-lived code returned after the player logs in.
  Your app exchanges this for tokens.
- **Access token** — A JWT valid for 20 minutes. Include it in the
  `Authorization: Bearer` header on authenticated ESI calls.
- **Refresh token** — Long-lived token used to get new access tokens without
  re-prompting the player.
- **Scopes** — Permissions your app requests (e.g., `esi-location.read_location.v1`).
  Players see these during authorization.

For the full SSO specification, see the [SSO documentation](../services/sso/index.md).

## Your First Authenticated Call

This script runs the complete OAuth2 flow:

1. Starts a local HTTP server to receive the callback
2. Opens your browser to the EVE SSO login page
3. Captures the authorization code after you log in
4. Exchanges it for access and refresh tokens
5. Reads your character's current solar system

!!! important

    Replace `your-client-id` and `your-client-secret` with the values from your
    registered application on [developers.eveonline.com](https://developers.eveonline.com/).

--8<-- "snippets/getting-started/authenticated-call.md"

Run it:

=== "Python"

    ```bash
    python authenticated-call.py
    ```

=== "TypeScript"

    ```bash
    npx tsx authenticated-call.ts
    ```

Your browser opens the EVE SSO login. After you authorize, the script prints:

```
Opening browser for EVE SSO login...

Capsuleer Name is in solar system 30000142
```

!!! tip

    Solar system IDs map to names via the public endpoint
    `GET /v3/universe/systems/{system_id}/`. Try adding a second call to resolve
    the system name!

## Token Refresh

Access tokens expire after **20 minutes**. Rather than asking the player to log
in again, use the refresh token to get a new access token silently.

### Token Lifecycle

``` mermaid
graph TD
    A[Access Token] --> B{Expired?}
    B -->|No| C[Make API Call]
    B -->|Yes| D[Use Refresh Token]
    D --> E[POST to Token Endpoint]
    E --> F[New Access + Refresh Tokens]
    F --> C
```

!!! warning

    Each refresh returns a **new refresh token**. Always store the latest one.
    Using an old refresh token will fail.

### How to Detect Expiry

The access token is a JWT. Decode the payload to read the `exp` (expiration)
claim — a Unix timestamp. Compare it to the current time with a small buffer
(60 seconds) to avoid race conditions.

### How to Refresh

Send a `POST` to the token endpoint with:

- `grant_type=refresh_token`
- `refresh_token=<your_refresh_token>`
- HTTP Basic authentication (`client_id:client_secret`, base64-encoded)

The response contains a new `access_token` and `refresh_token`.

### Refresh Utilities

These helper functions handle the full lifecycle — check expiry, refresh when
needed, and return a valid token:

--8<-- "snippets/getting-started/token-refresh.md"

Use `ensure_valid_token()` before every API call:

=== "Python"

    ```python
    access_token, refresh_token = ensure_valid_token(
        access_token, refresh_token, CLIENT_ID, CLIENT_SECRET
    )
    ```

=== "TypeScript"

    ```typescript
    const [accessToken, refreshToken] = await ensureValidToken(
      accessToken, refreshToken, CLIENT_ID, CLIENT_SECRET
    );
    ```

!!! note

    In a real application, persist tokens to disk or a database so they survive
    restarts. The refresh token remains valid until the player revokes your
    application's access.

## Next Steps

You now have a working foundation for EVE third-party development. Here's where
to go from here:

- **[Rate Limiting](../services/esi/rate-limiting.md)** — Understand ESI's error
  rate limiting and how to stay within limits
- **[SSO Documentation](../services/sso/index.md)** — Full SSO specification
  including JWT validation and PKCE for public clients
- **[Pagination](../services/esi/pagination/cursor-based.md)** — Handle endpoints
  that return paginated results
- **[Community Showcase](../community/index.md)** — See what others have built
  and find libraries for your language
- **[Static Data](../services/static-data/index.md)** — Bulk game data for
  items, systems, blueprints, and more
- **[EVE Developers Discord](https://discord.gg/eveonline)** — Get help from
  the community (#devfleet channel)
