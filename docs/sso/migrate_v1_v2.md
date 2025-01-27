<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

# Migrating from SSO v1 to v2

This document provides a general outline of the steps required for migrating from SSO v1 to SSO v2. Not all steps mentioned here will be 100% applicable for all use cases but should be generic enough to adjust for a variety of situations.

More details about the v1 deprecation can be found in [this blog post](https://developers.eveonline.com/blog/article/sso-endpoint-deprecations-2)

## Outline

1. Use form encoding for `/oauth/token` requests. JSON and Query String are no longer supported
2. Always update your stored refresh token with the latest received from the `/oauth/token endpoint`
3. Change the base url from `login.eveonline.com` to `login.eveonline.com/v2`
4. Replace calls to `/oauth/verify` with local decode and optional verification

The migration steps don't have to be implemented in this exact order, but doing so has some advantages, such as making an explicit token migration unnecessary. Old v1 refresh_tokens will simply be replaced with the new v2 token on the first refresh.

----

## 1. Use form encoding for token requests

The SSO v1 endpoints supported requests using a number of different payload formats, including JSON and URL Query String. SSO v2 enforces the payload to be sent in the body as an url-encoded string, with the `Content-Type: application/x-www-form-urlencoded` header.

In most modern HTTP clients, changing that should be trivial. For example, making the change in Python `requests` looks like this:

```python
payload = {"client_id": 12345678, grant_type: "authorization_code" [...]}

# From this
- requests.post("https://login.eveonline.com/oauth/token", json=payload)

# To this
+ requests.post("https://login.eveonline.com/v2/oauth/token", data=payload)
```

## 2. Update stored refresh token

Since there is no one standard way to handle caching and storing tokens there's no code example for this step. The mechanism that's needed is that every time a POST request is made to `/v2/oauth/token` with a refresh token and `grant_type=refresh_token` the stored refresh token has to be replaced with the refresh token provided in the response to that request.

This step is necessary for two purposes. On the one hand it future-proofs your application for an expected upcoming change to SSO which will introduce rotating refresh tokens. On the other hand it removes the need for a dedicated v1 to v2 token migration process, since v1 tokens will just be replaced with their v2 equivalent on the first refresh. Note that this only applies if your application regularly refreshes tokens. If you only very occasionally have a need for refreshing tokens you may still need a dedicated migration process to ensure all tokens are refreshed while the v1->v2 upgrade is possible.

## 3. Change base url

This change ensures that you're using the v2 routes for all SSO endpoints. Since EVE SSO follows the OAuth2 standards for all its routes most OAuth2 clients will use the correct routes by just changing the base URL from `https://login.eveonline.com` to `https://login.eveonline.com/v2`.

If your application does the OAuth2 flow manually or has the routes defined explicitly, the following routes have to be changed:

- From `https://login.eveonline.com/oauth/authorize`  
  To `https://login.eveonline.com/v2/oauth/authorize`
- From `https://login.eveonline.com/oauth/token`  
  To `https://login.eveonline.com/v2/oauth/token`

The `https://login.eveonline.com/oauth/verify` endpoint is being removed, see step 4 for detais.

## 4. Decode token locally

This replaces the call to `https://login.eveonline.com/oauth/verify`. It is strongly suggested that you use an existing JWT library for this purpose. Signature verification won't be covered in this guide since it's not necessary for most uses cases where the token is received directly from the EVE SSO servers.

Data provided by the verify endpoint included the expiration date of the token, scopes granted, identification of the character and the owner hash. All that data is included in the token and can be manually decoded the way shown below. 

```python
from base64 import urlsafe_b64decode
import json

token = "ey<...>n0.eyJ<...>In0.fh0<...>-WKA"

# Split the token into its encoded components
[header,payload,verify] = token.split(".")

# Pad the payload and decode
padded = payload + "="*(-len(payload) % 4)
decoded = urlsafe_b64decode(padded)
data = json.loads(decoded)
```

To turn this into a format that more closely matches the format used by the `/oauth/verify` endpoint a little bit of reformatting is needed:

```python
from datetime import datetime

{
  "CharacterID": data["sub"].split(":")[2],
  "CharacterName": data["name"],
  "ExpiresOn": datetime.fromtimestamp(data["exp"]).isoformat(),
  "Scopes": data["scp"],
  "TokenType": "JWT",
  "CharacterOwnerHash": data["owner"],
  "ClientID": data["azp"]
}
```

## Additional considerations

* JWT Tokens can get quite large. If you're storing the access token in a limited-size field you may have to adjust your schema if you use a large number of scopes