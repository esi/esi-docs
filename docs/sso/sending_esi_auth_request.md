# Sending an authenticated request to ESI
This documentation explains how to send an authenticated request to ESI after having gotten an access token from the [web based OAuth flow](web_based_sso_flow.md) or the [mobile/desktop OAuth flow](native_sso_flow.md). It is assumed you have gone through one of these and have acquired a valid access token that has the correct scopes applied.

After having retrieved a valid access token from EVE's SSO, add the following header to any request to an authenticated ESI route:

    Authorization: Bearer <access token>

where you will replace any text between `<>`, including `<>` with the actual access token.

As an example, if you wanted to get CCP Zoetrope's blueprints and you had a valid access token, you would make the following request:

    GET https://esi.evetech.net/latest/characters/2112625428/blueprints/

    Authorization: Bearer <access token>

where all text between `<>`, including `<>` should be replaced with the actual access token.
