## Refreshing tokens

If any valid scope was requested in the initial redirect to the SSO using the authorization code flow, a refresh token will be returned by the token endpoint, along with the access token. While the access token will expire after the listed interval, the refresh token can be stored and used indefinitely. Users can revoke access for individual apps on the [support site](https://community.eveonline.com/support/third-party-applications/).

To get a new access token you must make a POST request to `https://login.eveonline.com/v2/oauth/token` with the following parameters:

- grant_type: Must be set to "refresh_token".
- refresh_token: The refresh token received from the last request to the token endpoint.
- scope **[OPTIONAL]**: a subset of the original scopes assigned to the authorization and refresh token. If omitted, all original scopes will be assigned to the new access token.

>You also need to include an Authentication header ([basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) with the client ID as the username and secret key as the password).
>
>**This is currently a bug as 3rd party developers shouldn't need to authorize to use refresh tokens. That will be fixed before official release.**

The request should look like this:

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

>**Please make sure that the `refresh_token` value returned might not be the same as was sent in (typical if a server implements refresh_token rotation.). Make sure to update the refresh token stored on the client side in those cases.**
