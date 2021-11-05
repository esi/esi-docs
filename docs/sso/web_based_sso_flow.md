# OAuth 2.0 for Web Based Applications
*Note: This document assumes you have read the [basics of SSO authorization](sso_authorization_flow.md).*

This document will cover the implementation details you will need to know for your web based application to be able to complete the OAuth 2.0 flow with EVE's Single Sign On (SSO). This is required to access authenticated ESI routes.

## Overview of OAuth 2.0 flow for web based Applications

When doing the OAuth 2.0 flow with the EVE SSO, web based applications should be using [basic authentication](https://swagger.io/docs/specification/authentication/basic-authentication/).

Here is the OAuth 2.0 flow your web based application should be implementing:

1. [Create a new application](creating_sso_application.md) on the EVE SSO.

2. Store the `Client ID` and `Secret Key` assigned to your application somewhere that is accessible by your application. **The `Secret Key` in particular needs to be stored securely and should never be shared**.

<details><summary>⚠️Serenity note</summary>
- Before user's SSO flow, you must request a device id using https://mpay-web.g.mkey.163.com/device/init with following parameters in the [query string](https://en.wikipedia.org/wiki/Query_string). Make sure all strings placed in the URL are [URL Encoded](https://en.wikipedia.org/wiki/Percent-encoding).

   * `game_id=aecfu6bgiuaaaal2-g-ma79` - Hardcoded value

   * `device_type=PC`  - Hardcoded value

   * `system_name=<OS type>` - User's OS name, it can be `Windows` or `MacOS` or `Linux` or anything

   * `system_version=<OS version>` - User's OS version

   * `device_model=<architecture>` - User's OS architecture, it can be `32` or `64`

   * `resolution=<screen resolution>` - User's screen resolution, eg: `1024*768`

   The response will like this 

        {
            "code": 0,
            "device": {
                "id": "<device_id>",
                "key": "xxxx",
                "urs_device_id": "xxxx"
            },
            "msg": "ok"
        }

   Store the `<device_id>` to your application session store. 

</details>
 
3. Prepare the authorize URL https://login.eveonline.com/v2/oauth/authorize/ (or https://login.evepc.163.com/v2/oauth/authorize/ if you are working for Serenity) with the following parameters in the [query string](https://en.wikipedia.org/wiki/Query_string). Make sure all strings placed in the URL are [URL Encoded](https://en.wikipedia.org/wiki/Percent-encoding).

    * `device_id=<device id>` - For Serenity ONLY, device id requested from notes before, if `device_id` is the first parameter, change it to `&device_id`. (See [issue](https://github.com/ccpgames/sso-issues/issues/64))

    * `response_type=code` - This tells the EVE SSO what kind of response you are expecting from it, in this case you are letting it know you are starting the handshake for an authorization code.

    * `redirect_uri=<your application's defined callback>` - Replace all text after the `=` with the full callback URL you defined for you application when [creating a new application](creating_sso_application.md), make sure it is URL encoded (e.g. https%3A%2F%2Flocalhost%2Fcallback%2F). **If you put in any other URL other than what is defined in your SSO application the EVE SSO will reject your request**.

    * `client_id=<your application's client ID>` - Replace all text after the `=` with the client ID assigned to your application that you stored somewhere in step 2.

    * `scope=<A URL encoded, space delimited list of ESI scopes you would like to request permissions for>` - Replace all text after the `=` with a list of esi scopes split up by a single space that you would like to request permissions for (e.g. `scope=esi-characters.read_blueprints.v1%20esi-corporations.read_contacts.v1`).

    * `state=<something-unique>` - Replace all text after the `=` with a unique string of your choice. `state` is required by EVE's SSO to encourage extra security measures. A good explanation about how your application can be more secure with the use of the `state` parameter can be found [here](https://auth0.com/docs/protocols/oauth2/oauth-state).

    If you wanted access to a character's blueprints and your callback URL was `https://localhost/callback/` you would have a URL that looks something like this (anything surrounded by `<>` should be replaced by you, including `<>`): `https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri=https%3A%2F%2Flocalhost%2Fcallback%2F&client_id=<your-client-id>&scope=esi-characters.read_blueprints.v1&state=<unique-string>`.

4. If you are working for Tranquility, redirect your user to the URL prepared in step 3.

<details><summary>⚠️Serenity note</summary>

- If you are working for Serenity, redirect your user to https://login.evepc.163.com/account/logoff with following parameters in the [query string](https://en.wikipedia.org/wiki/Query_string). Make sure all strings placed in the URL are [URL Encoded](https://en.wikipedia.org/wiki/Percent-encoding).

   * `returnUrl=<URL encoded authorize URL>` - URL prepared in step 3. (workaround for [issue](https://github.com/ccpgames/sso-issues/issues/49))
</details>

5. The EVE SSO will send a GET request to your application's defined callback URL containing the query parameters `code` and `state` that looks like this (anything between `<>` will look different for you): `https://<your-callback-url>/?code=<super-secret-code>&state=<unique-state-string-from-you>`.

    Your application needs to lift the value of the `code` query parameter from the URL so that it can be used in the next step. This authorization code is a one time use only token that has a lifetime of 5 minutes. If you do not respond within 5 minutes you will have to start over at step 1 again.

6. Now that your application has the authorization code, it needs to send a POST request to `https://login.eveonline.com/v2/oauth/token` (or `https://login.evepc.163.com/v2/oauth/token` if you are working for Serenity) with a payload containing the authorization code using [Basic authentication](https://swagger.io/docs/specification/authentication/basic-authentication/) where your application's client ID will be the user and your secret key will be the password. Here is a little more detail on how to craft this request:

* Create form encoded values that look like this (replace anything between `<>`, including `<>`):

        grant_type=authorization_code&code=<authorization code from callback URL>

* Create a URL safe Base64 encoded string where the contents before encoding are your application's client ID, followed by a `:`, followed by your application's secret key (e.g. `URL safe Base64(<client_id>:<secret_key>)`).

    * You will need to send the following HTTP headers (replace anything between `<>`, including `<>`):
        * `Authorization: Basic <URL safe Base64 encoded credentials>`
        * `Content-Type: application/x-www-form-urlencoded`
        * `Host: login.eveonline.com`

* Finally, send a POST request to `https://login.eveonline.com/v2/oauth/token` (or `https://login.evepc.163.com/v2/oauth/token` if you are working for Serenity) with your form encoded values and the headers from the last step.


7. If the previous step was done correctly, the EVE SSO will respond with a JSON payload containing an access token (which is a [Json Web Token](https://jwt.io/introduction/)) and a refresh token that looks like this (Anything wrapped by `<>` will look different for you):

        {
            "access_token": <JWT token>,
            "expires_in": 1199,
            "token_type": "Bearer",
            "refresh_token": <unique string>
        }

    For added security, before trusting the access_token and refresh_token, you should [validate the access token](validating_eve_jwt.md) to make sure it has not been tampered with in transit from the SSO to your application.

    Once validated, your application will need to store both the access token and refresh token from this payload. **Store the refresh token somewhere secure and never share it**.

    *Note on security: the access token should also be stored securely but if it were to get leaked it can only be used for as long as is left of its 20 minute lifetime. If your refresh token gets leaked it can only be invalidated by you, the application developer, by [revoking it](revoking_refresh_tokens.md). **If you know your refresh token has been leaked you must revoke it**.*

The following diagram is a visual representation of the steps above. Any number between brackets (`[]`) is a reference to a step number in the list above:

![Web based OAuth 2.0 Flow Diagram](img/web_oauth_flow.svg)

If any of this is confusing, there is a [code example](https://github.com/esi/esi-docs/blob/master/examples/python/sso/esi_oauth_web.py) available in Python that you can run locally to see this flow in action.

## Further reading
You can continue by reading about [how to send an authorized request to ESI](sending_esi_auth_request.md) or you can read about [how to get a new access token using your refresh token](refreshing_access_tokens.md).
