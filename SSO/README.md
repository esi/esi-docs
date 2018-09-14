# SSO

## What is the SSO
Single Sign On (SSO) services are a way for users to log into one web site using their username and password from a different web site. For example, any time you log into a website using your Facebook account you are interacting with Facebook's SSO.

In EVE Online's case, you can use their SSO to allow users of your application to authenticate against EVE's servers using a method called [OAuth2](https://oauth.net/2/). This means that your application will never deal with that user's username or password for EVE.

## Table of contents
[High level overview of SSO authorization flow](sso_authorization_flow.md)

[Creating an EVE Online SSO application](creating_sso_application.md)

[OAuth 2.0 for web based applications](web_based_sso_flow.md)

[OAuth 2.0 for desktop/mobile applications](native_sso_flow.md)

[Refreshing access tokens](refreshing_access_tokens.md)

[Validating EVE SSO JWT tokens](validating_eve_jwt.md)

[Sending authenticated requests to ESI](sending_esi_auth_request.md)

### How to read this documentation
Start by reading the high level overview of the [OAuth 2.0 flow with the EVE SSO](sso_authorization_flow) and then follow the links there that apply to your specific application for more detailed instructions.

### Singularity SSO
All instances of https://login.eveonline.com found in this documentation can be swapped for https://sisilogin.testeveonline.com if you are developing against EVE's Singularity test server.

### Login Images
When creating a button to direct users to login to your site or application with the EVE SSO please use one of the following images for the button. This helps create consistency for EVE players amongst all third party applications when viewing your site or application.

![EVE SSO Login Buttons Large White](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-white-large.png)

![EVE SSO Login Buttons Large Black](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-black-large.png)

![EVE SSO Login Buttons Small White](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-white-small.png)

![EVE SSO Login Buttons Small Black](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-black-small.png)

## Community and Bug Reports
If you want real time help with using SSO join the [tweetfleet slack](https://www.fuzzwork.co.uk/tweetfleet-slack-invites/) and navigate to the #sso channel.

If you run into an issue when using EVE's SSO you can report these issues at https://github.com/ccpgames/sso-issues.
