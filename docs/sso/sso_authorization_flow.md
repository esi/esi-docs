<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

# SSO Authorization Flow

This page covers the basic concepts of the authorization flow your application will need to perform with EVE's Single Sign On (SSO). This is meant to be a high level overview and the more specific instructions are linked to at the end of this page.

In order to access authenticated ESI routes for you or other user's characters your application will need to follow the [OAuth 2.0](https://oauth.net/2/) protocol (more specifically using the [Authorization code grant type](https://oauth.net/2/grant-types/authorization-code/)).


Here is the basic OAuth 2.0 flow, details are omitted for the sake of simplicity that other documentation found here will cover:

1. Your application will redirect a user to a login page provided by EVE's SSO.

2. After a user logs in as a specific character the SSO will send a GET request to a URL provided by your application containing a one use only authorization code that expires in 5 minutes (you define this callback URL when [Creating an SSO Application](creating_sso_application.md)).

3. After receiving the authorization code from EVE's SSO, your application will make one more request to the SSO that contains this code.

4. If step 3 is successful, the SSO will respond with an access token whose lifetime is 20 minutes as well as a refresh token that can be used to get another access token in the future. This access token and refresh token will be valid for the user's character using the scopes defined in step 2.

5. Your application can now include this access token when making a request to access authenticated resources as long as the correct scope applies to that ESI route.

6. Once the access token expires in 20 minutes, your application will send another request to the SSO using the refresh token from step 3 to get a new access token.

The following diagram is a visual representation (with slightly more detail) than the steps listed above. Any numbers wrapped in brackets (`[]`) represent which of the above steps are encapsulated by the visual representation.

![Simplified OAuth2 Flow](img/simple_flow.svg)

As can be seen, there are three tokens that are particularly important to have a good understanding about from the flow listed above: the **authorization code**, **access token** and **refresh token**. Because it is so important to have a grasp of what these three tokens are used for, here is a recap:

* **Authorization code** - A one time use only code sent to your application's defined callback URL from the EVE SSO whose lifetime is 5 minutes. This code is used to prove you are the application who initiated the handshake.

* **Access token** - A token returned from the EVE SSO in exchange for the authorization code. This token's lifetime is 20 minutes and grants access to authenticated ESI routes whose scopes match the access token.

* **Refresh token** - A token returned from the EVE SSO in exchange for the authorization code. This token lasts as long as the application does not revoke it and **needs to be stored in a secure place**. The refresh token can be exchanged for new access tokens once their lifetime has ended.

## Implementing OAuth 2.0 for Your Applications

Now that you understand the basic flow of OAuth 2.0, you can continue on to more detailed documentation that will teach you how to actually apply it to your application. We suggest slightly different ways of executing OAuth 2.0 depending on what type of application you're building. These two distinctions are whether you're building a mobile/desktop application or a web based application. **It is important to follow the instructions that apply to the application type you are building as the different flows shown will become mandatory and enforced sometime in the future by the EVE SSO.**

Click on your application type to begin:

* [My application is web based and accessible from a browser](web_based_sso_flow.md)
* [My application is a mobile or desktop application](native_sso_flow.md)
