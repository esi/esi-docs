# Revoking Refresh Tokens
*Note: This documentation assumes you have read the [basic SSO flow](sso_authorization_flow.md) and that you understand what a refresh token is used for.*

If you know your refresh token has been compromised, it is important to revoke it. This documentation will show you have to do that and you can read [RFC 7009](https://tools.ietf.org/html/rfc7009) if you want to dig into even more details.

1. Find EVE SSO's revocation endpoint by making a GET request to its meta route which can be found at URL `https://login.eveonline.com/.well-known/oauth-authorization-server`. You will get a response similar to this:

    ```json
    {
        "issuer": "login.eveonline.com",
        "authorization_endpoint": "https://login.eveonline.com/v2/oauth/authorize",
        "token_endpoint": "https://login.eveonline.com/v2/oauth/token",
        "response_types_supported": [
            "code",
            "token"
        ],
        "jwks_uri": "https://login.eveonline.com/oauth/jwks",
        "revocation_endpoint": "https://login.eveonline.com/v2/oauth/revoke",
        "revocation_endpoint_auth_methods_supported": [
            "client_secret_basic",
            "client_secret_post",
            "client_secret_jwt"
        ],
        "token_endpoint_auth_methods_supported": [
            "client_secret_basic",
            "client_secret_post",
            "client_secret_jwt"
        ],
        "token_endpoint_auth_signing_alg_values_supported": ["HS256"],
        "code_challenge_methods_supported": ["S256"]
    }
    ```

    From here you want to get the value of the key `revocation_endpoint`, which at this time of writing is `https://login.eveonline.com/v2/oauth/revoke`.

2. Make a POST request to the revocation endpoint retrieved from step 1 using [basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication), where your application's client ID is the user and your application's secret key is the password, with the form encoded body:

    ```
    token_type_hint=refresh_token&token=<your refresh token to revoke>
    ```

    Replace all text wrapped with `<>` with a value provided by you.

    Make sure to set the correct Content-Type header:

    ```
    Content-Type: application/x-www-form-urlencoded
    ```

3. The server responds with a 200 OK response code. If you submitted a valid token, the server has now invalidated it. Note that the server also returns a 200 OK if the token was invalid, because in both cases the end result is the same - you are not able to use the token to successfully request a new access token.


If you'd like to look at an example of revoking a refresh token written in Python you can find one [here](https://github.com/esi/esi-docs/blob/master/src/main/python/sso/revoke_refresh_token.py).
