# Introduction
## What is the SSO
Single Sign On (SSO) services are a way for users to log into one web site using their username and password from a different web site. For example, any time you log into a website using your Facebook account you are interacting with Facebook's SSO.

In EVE Online's case, you can use their SSO to allow users of your application to authenticate against EVE's servers using a method called [OAuth2](https://oauth.net/2/). This means that your application will never deal with that user's username or password for EVE.

## Key Concepts
There are two key concepts related to SSO you will have to become familiar with as a third party developer to be able to make authenticated requests to ESI on behalf of other EVE users. The following concepts are covered in this documentation:

* **OAuth2 authorization protocol** - This is how your app will interact with EVE's SSO. This is discussed in more detail in [SSO Authorization Flow](sso_authorization_flow.md).

* **SSO Scopes** - As an application developer you will need to ask for permission to access certain kinds of data from your user's EVE Online characters. In SSO terms these permissions are called scopes and different authenticated endpoints use different scopes. Scopes allow your application to ask for permission to view only subsets of a character's data rather than getting access to all info about that character. Scopes are discussed at more length in [Creating an SSO Application](#TODO add this link once you have it).


## Registering for the SSO
To use the SSO in your app, you must first register it at [the developers site](https://developers.eveonline.com/). When you create a new application here it will give you a client ID and secret key, which are used in the authentication flow.

You are required to supply the following:
- Name: Name of the application, will be displayed to the users when asked to authorize your app.
- Description: Description of the application, will be listed under your app in [Third Party Applications](https://community.eveonline.com/support/third-party-applications/).
- Connection type: Can be API Access or Authentication Only. If API Access is selected, you will also need to select the scopes your app will use.
- Callback URL: Callback URL, which is the only location the login server will redirect back to after the user has authorized the login (See [Authentication flow](authentication.md) for details.)

### Errors
Please note:

If too many HTTP requests are done to an SSO endpoint within a set time interval the SSO will return a HTTP 409 response (being vague on the number of requests and time on purpose as we will be tuning these values).

### Test Server
All instances of https://login.eveonline.com can be swapped for https://sisilogin.testeveonline.com when trying to use Sisi.

### Login Images
When creating a button to direct users to login to your site or application with the EVE SSO please use one of the following images for the button. This helps create consistency for EVE players and when they view your site or application will more easily be able to quickly identify that it supports the EVE SSO.

![EVE SSO Login Buttons Large White](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-white-large.png)

![EVE SSO Login Buttons Large Black](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-black-large.png)

![EVE SSO Login Buttons Small White](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-white-small.png)

![EVE SSO Login Buttons Small Black](https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-black-small.png)
