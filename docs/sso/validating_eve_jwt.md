# Validating JWT tokens from the EVE SSO

This documentation assumes you have read through either the [web based OAuth 2.0 flow](web_based_sso_flow.md) or the [mobile/desktop OAuth 2.0 flow](native_sso_flow.md).

Your application should validate the access tokens received from the EVE SSO. There are many libraries for most programming languages available and listed on [JWT.IO](https://jwt.io). Auth0 also has a good and detailed introduction to [JWT token validation](https://auth0.com/docs/api-auth/tutorials/verify-access-token).

Listed below are the most important things to validate when using the JWT tokens issued by the EVE Online SSO. To explain, here is the payload from a typical SSO JWT Token.

```json
{
  "scp": [
    "esi-skills.read_skills.v1",
    "esi-skills.read_skillqueue.v1"
  ],
  "jti": "998e12c7-3241-43c5-8355-2c48822e0a1b",
  "kid": "JWT-Signature-Key",
  "sub": "CHARACTER:EVE:123123",
  "azp": "my3rdpartyclientid",
  "tenant": "tranquility",
  "tier": "live",
  "region": "world",
  "aud": ["my3rdpartyclientid", "EVE Online"],
  "name": "Some Bloke",
  "owner": "8PmzCeTKb4VFUDrHLc/AeZXDSWM=",
  "exp": 1648563218,
  "iat": 1648562018,
  "iss": "login.eveonline.com"
}
```

## Validating an EVE SSO JWT token

You will need to ensure four things when validating a JWT token from the EVE SSO:

1. ### Validate the JWT signature

    The [SSO metadata endpoint](https://login.eveonline.com/.well-known/oauth-authorization-server) contains a description of the supported operations for the SSO. That endpoint lists the supported endpoints as well as provides a link to the SSO JWT key set which is currently located at <https://login.eveonline.com/oauth/jwks>. You will need to load that key set using whatever JWT library available. Currently the SSO uses the RS-256 signature method, but will also support ES-256 in the near future.

1. ### Validate the issuer

    The issuer will either be the host name or the URI of the SSO instance you are using (e.g. `"login.eveonline.com"` or `"https://login.eveonline.com"`). Your application should handle looking for both the host name and the URI in the `iss` claim and should reject any JWT tokens where `iss` does not equal the host name or URI of EVE's SSO.

1. ### Validate the expiry date

    The `exp` claim contains the expiry date of the token as a UNIX timestamp. You can use that to know when to refresh the token and to make sure that the token is valid.

1. ### Validate the audience claim

    The `aud` claim contains the audience and must included both the `client_id` and the string value: `"EVE Online"`

You can look [here](https://github.com/esi/esi-docs/blob/master/examples/python/sso/validate_jwt.py) for a code example in Python showing you how to validate a JWT token.
