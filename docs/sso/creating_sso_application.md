<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

# Creating an SSO Application

Before you can make authenticated calls to ESI, the first step you must take is to create an EVE SSO Application.

To do this, navigate to EVE Online's [developer site](https://developers.eveonline.com/) and login with your EVE Online account. Once you've logged in, click on *Applications* on the top toolbar. View and accept the developers license if prompted and on the next page click *Create New Application*. This will redirect you to a form to fill out to for your application.

Fill in the *Name* and *Description* fields with relevant information about your application. In the section labelled *Connection Type* select *Authentication & API Access*. This
particular connection type is used for access to ESI.

Once this connection type is selected, a list of available scopes will be presented under the heading *Permissions*. Go over the list presented in the *Available Scopes List* and make educated choices about which scope your application really needs. **You should hardly ever need all scopes. We highly discourage you from asking for all scopes from your users**.

One way to figure out which scopes your application really needs is by going to the [ESI UI](https://esi.evetech.net/ui), finding the route you need access to, clicking on that route and seeing which scope it requires. Here is how it looks for the [/character/{character_id}/blueprints/](https://esi.evetech.net/ui/#/Character/get_characters_character_id_blueprints) route:

![Blueprint scope](img/blueprint_scope.png)

Once you know your application needs a particular scope, simply click on it and it will be moved over to the *Requested Scopes List*. If you change your mind you can always click it again and it will return to *Available Scopes List*.

Next, in the *Callback URL* field, enter the URL your application will use as its callback (explained in more detail in our [SSO flow documentation](sso_authorization_flow.md)). You can start by using `https://localhost/callback/` during development (and is what the documentation in this repository uses). However, **never use localhost as a callback URL for an application you have released.** You can always edit the callback URL after you have defined it.

Click the *Create Application* button to finish. Once the application has been created click on *View Application* to be able to see your application's client ID and secret key. This is also where you can update details about your application (such as adding scopes) or change the callback URL.

*Note: if you update the scopes needed for your application it will invalidate your refresh token and you will have to do the whole [SSO flow](sso_authorization_flow.md) from the beginning. This means making your users login again.*
