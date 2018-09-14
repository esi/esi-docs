## Refreshing tokens

If any valid scope was requested in the initial redirect to the SSO using the authorization code flow, a refresh token will be returned by the token endpoint, along with the access token. While the access token will expire after the listed interval, the refresh token can be stored and used indefinitely. Users can revoke access for individual apps on the [support site](https://community.eveonline.com/support/third-party-applications/).

To get a new access token you must make a POST request to `https://login.eveonline.com/v2/oauth/token` with the following parameters:

- `grant_type=refresh_token`

- `refresh_token=<refresh token from previous request to token endpoint>`: Replace everything after `=` with your own value.

- `scope=<subset of scopes from the original OAuth 2.0 flow>` **[OPTIONAL]**: Replace everything after `=` with your own value. A subset of the original scopes assigned to the authorization and refresh token. If omitted, all original scopes will be assigned to the new access token.

>If your application is web based (and you followed the [web based sso flow](web_based_sso_flow.md)) you also need to include an Authentication header ([basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) with the client ID as the username and secret key as the password).

The request should look like this (**don't include the `Authorization` header if your application is a mobile or desktop application**):

```http
POST https://login.eveonline.com/v2/oauth/token HTTP/1.1

Authorization: Basic bG9...ZXQ=
Content-Type: application/x-www-form-urlencoded
Host: login.eveonline.com

grant_type=refresh_token&refresh_token=gEy...fM0
```

The response should contain details about the new access token for that user. Example:

```json
{
  "access_token":"MXP...tg2",
  "token_type":"Bearer",
  "expires_in":1200,
  "refresh_token":"gEy...fM0"
}
```

>**Please note that the `refresh_token` returned may not be the same as the refresh token submitted. At some point in the future the EVE SSO will enable refresh token rotation for native applications. Make sure to update the refresh token stored on the client side in those cases.**
