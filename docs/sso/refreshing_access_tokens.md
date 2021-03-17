# Refreshing tokens

If any valid scope was requested in the initial redirect to the SSO using the authorization code flow, a refresh token will be returned by the token endpoint, along with the access token. While the access token will expire after the listed interval, the refresh token can be stored and used indefinitely. Users can revoke access for individual apps on the [support site](https://community.eveonline.com/support/third-party-applications/).

The method for refreshing access tokens is dependent on whether your application is a [web based](web_based_sso_flow.md) or [native](native_sso_flow.md) (e.g mobile/desktop) application. Jump to the section below that applies to your application.

## Web Based Applications
As a web based application you will need to make a URL-encoded POST request to `https://login.eveonline.com/v2/oauth/token` using [basic authentication]((https://en.wikipedia.org/wiki/Basic_access_authentication)) where your application's client ID is the user and your secret key is the password.

You will need to pass the following parameters:

- `grant_type=refresh_token`

- `refresh_token=<refresh token from previous request to token endpoint>`: Replace everything after `=` with your own value.

- `scope=<subset of scopes from the original OAuth 2.0 flow>` **[OPTIONAL]**: Replace everything after `=` with your own value. A subset of the original scopes assigned to the authorization and refresh token. If omitted, all original scopes will be assigned to the new access token.

You will need to pass the following HTTP headers:

- `Content-Type: application/x-www-form-urlencoded`
- `Host: login.eveonline.com`
- `Authorization: Basic <base64 encoded string containing your client ID and secret key joined by a single colon (:)>`: Replace everything after `Basic ` with the content described between `<>`.

The request should look like something like this:

```http
POST https://login.eveonline.com/v2/oauth/token HTTP/1.1

Content-Type: application/x-www-form-urlencoded
Host: login.eveonline.com
Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l  

grant_type=refresh_token&refresh_token=gEy...fM0
```

Remember that the refresh token *must* be URL-encoded, per the content type of the request. Failing to do this may cause the request to be malformed and a 400 response to be returned.

## Native Applications
As a native application you will need to make a URL-encoded POST request to `https://login.eveonline.com/v2/oauth/token` containing the following parameters:

- `grant_type=refresh_token`

- `refresh_token=<refresh token from previous request to token endpoint>`: Replace everything after `=` with your own value.

- `client_id=<your application's client ID>`: Replace everything after `=` with the client ID assigned to your application.

- `scope=<subset of scopes from the original OAuth 2.0 flow>` **[OPTIONAL]**: Replace everything after `=` with your own value. A subset of the original scopes assigned to the authorization and refresh token. If omitted, all original scopes will be assigned to the new access token.

You will need to pass the following HTTP headers:

- `Content-Type: application/x-www-form-urlencoded`
- `Host: login.eveonline.com`

The request should look like something like this:

```http
POST https://login.eveonline.com/v2/oauth/token HTTP/1.1

Content-Type: application/x-www-form-urlencoded
Host: login.eveonline.com

grant_type=refresh_token&refresh_token=gEy...fM0&client_id=9f1...8d2
```

## SSO Response
The response from the SSO contains details about the new access token for that user and will look similar to this:

```json
{
  "access_token":"MXP...tg2",
  "token_type":"Bearer",
  "expires_in":1200,
  "refresh_token":"gEy...fM0"
}
```

>**Please note that the `refresh_token` returned may not be the same as the refresh token submitted. At some point in the future the EVE SSO will enable refresh token rotation for native applications. Make sure to update the refresh token stored on the client side in those cases.**
