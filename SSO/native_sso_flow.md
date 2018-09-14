# OAuth 2.0 for Mobile or Desktop Applications
*Note: This document assumes you have read the [basics of SSO authorization](sso_authorization_flow.md).*

This document will cover the implementation details you will need to know for your desktop or mobile application to be able to complete the OAuth 2.0 flow with EVE's Single Sign On (SSO). This is required to access authenticated ESI routes.

## Overview of OAuth 2.0 flow for native applications

When doing the OAuth 2.0 flow with the EVE SSO, native applications should use the [PKCE](https://www.oauth.com/oauth2-servers/pkce/) protocol.

Here is the OAuth 2.0 flow your native application should be implementing:

1. [Create a new application](creating_sso_application.md) on the EVE SSO.

2. Store the `Client ID` assigned to your application somewhere that is accessible by your application.

3. Redirect your user to https://login.eveonline.com/v2/oauth/authorize/ with the following parameters in the [query string](https://en.wikipedia.org/wiki/Query_string). Make sure all strings placed in the URL are [URL Encoded](https://en.wikipedia.org/wiki/Percent-encoding).

    * `response_type=code` - This tells the EVE SSO what kind of response you are expecting from it, in this case you are letting it know you are starting the handshake for an authorization code.

    * `redirect_uri=<your application's defined callback>` - Replace all text after the `=` with the full callback URL you defined for you application when [creating a new application](creating_sso_application.md), make sure it is URL encoded (e.g. https%3A%2F%2Flocalhost%2Fcallback%2F). **If you put in any other URL other than what is defined in your SSO application the EVE SSO will reject your request**.

    * `client_id=<your application's client ID>` - Replace all text after the `=` with the client ID assigned to your application that you stored somewhere in step 2.

    * `scope=<A URL encoded, space delimited list of ESI scopes you would like to request permissions for>` - Replace all text after the `=` with a list of ESI scopes split up by a single space that you would like to request permissions for (e.g. `scope=esi-characters.read_blueprints.v1%20esi-corporations.read_contacts.v1`).

    * `code_challenge=<URL safe Base64(SHA256(URL safe Base64(random 32 byte string)))>` - In the PCKE protocol, a code challenge is used instead of basic authentication to allow your application to ship without its secret key. The reason for this being to protect malicious actors from being able to decompile your programs and retrieve the secret key. A more detailed explanation of the kind of attacks this protects against can be found in [RFC7636](https://tools.ietf.org/html/rfc7636#section-1)

        To correctly create a code challenge your application will need to make a one time use only 32 byte random string. You will then URL safe Base64 encode this random string, then hash that and finally URL safe Base64 encode the hashed value. The resulting Base64 encoded string is the code challenge. Make sure you keep the original Base64 encoded random value for later as you will need to use that in step 5. If you'd like to see an example of creating a code challenge in Python you can find that [here](../examples/python/sso/esi_oauth_native.py). *Feel free to contribute examples in other languages to this repository to help others.*

    * `code_challenge_method=S256` - This is telling the EVE SSO that the code challenge was hashed using the [SHA-256 hashing algorithm](https://en.wikipedia.org/wiki/SHA-2) and is the only method currently accepted at this time.

    * `state=<something-unique>` - Replace all text after the `=` with a unique string of your choice. `state` is required by EVE's SSO to encourage extra security measures. A good explanation about how your application can be more secure with the use of the `state` parameter can be found [here](https://auth0.com/docs/protocols/oauth2/oauth-state).

If you wanted access to a character's blueprints and your callback URL was `https://localhost/callback/` you would have a URL that looks something like this (any text surrounded by `<>` should be replaced by you, including `<>`): `https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri=https%3A%2F%2Flocalhost%2Fcallback%2F&client_id=<your-client-id>&scope=esi-characters.read_blueprints.v1&code_challenge=<URL safe Base64(SHA256(URL safe Base64(random 32 byte string)))>&code_challenge_method=S256&state=<unique-string>`.

4. The EVE SSO will send a GET request to your application's defined callback URL containing the query parameters `code` and `state` that looks like this (anything wrapped by `<>` will look different for you): `https://<your-callback-url>/?code=<super-secret-code>&state=<unique-state-string-from-you>`.

    Your application needs to lift the value of the `code` query parameter from the URL so that it can be used in the next step. This authorization code is a one time use only token that has a lifetime of 5 minutes. If you do not respond within 5 minutes you will have to start over at step 1 again.

5. Now that your application has the authorization code, it needs to send a POST request to `https://login.eveonline.com/v2/oauth/token` with a payload containing the returned authorization code, the client ID of your application, and the original URL safe Base 64 encoded 32 byte string that was randomly created for the code challenge in step 3. *Note: you can look at a Python example of this returning a code verifier [here](../examples/python/sso/esi_oauth_native.py)*.

Here is a little more detail on how to craft this request:

* Create a JSON payload that looks like this (replace anything between `<>`, including `<>`):

            {
                "grant_type": "authorization_code",
                "code": <authorization code from callback URL>,
                "client_id": <your application's client ID>,
                "code_verifier": <URL safe Base64(32 byte string) generated in step 3>  
            }

* Send a POST request to `https://login.eveonline.com/v2/oauth/token` with your JSON payload and the following headers:

        * `Content-Type: application/x-www-form-urlencoded`
        * `Host: login.eveonline.com`

6. If the previous step was done correctly, the EVE SSO will respond with a JSON payload containing an access token (which is a [Json Web Token](https://jwt.io/introduction/)) and a refresh token that looks like this (anything wrapped by `<>` will look different for you):

        {
            "access_token": <JWT token>,
            "expires_in": 1199,
            "token_type": "Bearer",
            "refresh_token": <unique string>
        }

    For added security, before trusting the access_token and refresh_token, you should [validate the access token](validating_eve_jwt.md) to make sure it has not been tampered with in transit from the SSO to your application.

    Once validated, your application will need to store both the access token and refresh token from this payload. **Store the refresh token somewhere secure and never share it**.

    *Note: as a native application you should expect the refresh token to be volatile, meaning you should always be prepared to receive a new refresh token every time you refresh your access tokens.*

    *Note on security: the access token should also be stored securely but if it were to get leaked it can only be used for as long as is left of its 20 minute lifetime. If your refresh token gets leaked it can only be invalidated by you, the application developer, by [revoking it](revoking_refresh_tokens.md). **If you know your refresh token has been leaked you must revoke it**.*

The following diagram is a visual representation of the steps above. Any number between brackets (`[]`) is a reference to a step number in the list above:

![Native OAuth 2.0 Flow Diagram](img/native_oauth_flow.svg)

If any of this is confusing, there is a [code example](../examples/python/sso/esi_oauth_native.py) available in Python that you can run locally to see this flow in action.

## Further reading
You can continue by reading about [how to send an authorized request to ESI](sending_esi_auth_request.md) or you can read about [how to get a new access token using your refresh token](refreshing_access_tokens.md).
