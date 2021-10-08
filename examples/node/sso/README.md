# EVE SSO Example in node

## Example .env file

```
ESI_CLIENT=abc123
ESI_SECRET=abc123
```

## Prerequesites
1. Have node and yarn installed
1. Create an ESI application, with the callback url: `http://localhost:3000/api/auth/callback/eveonline`


## Startup Instructions
1. Create a `.env` file with the above keys, using your credentials
1. Run `yarn install`
1. Run `yarn start`
1. Visit http://localhost:3000/auth in your browser. You will be redirected to CCP to log in to your account
1. Complete the login, and you will receive the following response as json:

```json
{
  "token": {
    "access": "access token",
    "refresh": "refresh token"
  },
  "jwtResult": "an object of everything coming from verifying a jwt",
  "character": {
    "name": "character name",
    "owner": "owner hash for verifying that a user has not changed hands",
    "characterId": "character id"
  }
}
```
