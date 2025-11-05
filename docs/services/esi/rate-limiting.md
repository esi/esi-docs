---
title: Rate Limiting
---
# Rate Limiting

ESI implements [floating window rate limiting](https://smudge.ai/blog/ratelimit-algorithms#sliding-windows) to ensure fair usage across all applications.
The intention of the rate limit is to show third party developers where the line is; but please don't take it for a challenge to constantly find the line.
In most cases you should be fine with far less requests than the rate limit allows you.

!!! important

    Rate limiting isn't active on all routes yet.
    Check the OpenAPI Specs or the HTTP response headers for up-to-date information.

## Floating Window

A floating window is a mathematical approximation where tokens consumed by a request are released back to your bucket after the window size has passed.

For example, with a 15-minute window:

- If you make a request at 10:00 AM that costs 2 tokens, those 2 tokens will be returned to your bucket around 10:15 AM.
- If you make another request at 10:05 AM that costs 1 token, that token will be returned around 10:20 AM.

This creates a sliding window where your token consumption is tracked continuously, and tokens are freed up as time passes from when they were originally consumed.

## Bucket System

Each `rate limit group` and `userID` pair is assigned their own bucket.

- `rate limit group`: Each route is assigned to a rate limit group. This is mentioned both in the response headers as in the API specifications.
- `userID`:
    - Authenticated routes: `<applicationID>:<characterID>` from the Access Token.
    - Non-authenticated routes: `<sourceIP>` (or `<sourceIP>:<applicationID>` if an Access Token is supplied).

On each request, ESI verifies that you haven't exceeded the maximum tokens allocated for your assigned bucket.
If you have exceeded that limit, you receive a 429, together with a `Retry-After` header.
This header indicates, in seconds, when you will have enough tokens to make a request that won't be rate limited.

!!! note

    The reason the `userID` is a combination of both the `applicationID` and `characterID`, is to ensure popular apps have to obey by the same limits as newly created apps.
    Some token limits might look small, but remember: they are per applicationID/characterID pair.

## Token System

Every request consumes tokens based on the response status:

| Status Code | Token Cost | Reasoning                                              |
|-------------|------------|--------------------------------------------------------|
| 2XX         | 2 tokens   |                                                        |
| 3XX         | 1 token    | Promote the use of `If-Modified-Since` and `If-Match`. |
| 4XX         | 5 tokens   | Discourage hitting user-errors.                        |
| 5XX         | 0 tokens   | You shouldn't be penalized for server-side errors.     |

## Rate Limit Headers

The following headers are included in HTTP response for routes under rate limiting:

- `X-Ratelimit-Group`: Route group identifier.
- `X-Ratelimit-Limit`: Total tokens per window (format: `150/15m`).
    - `m`: minutes.
    - `h`: hours.
- `X-Ratelimit-Remaining`: Available tokens remaining.
- `X-Ratelimit-Used`: Tokens consumed by this request.

And if you are rate-limited (429):

- `Retry-After`: indicates, in seconds, when to try again.

## OpenAPI Specs extension

For each route that has rate limiting active, the OpenAPI specs announces this via the `x-rate-limit` extension.
This contains three fields:

- `group`: the rate limit group this route belongs to.
- `window-size`: the size of the window.
- `max-tokens`: the maximum amount of tokens allowed per `window-size`.

Each route in the same group will show the same `window-size` and `max-tokens`.

## Best Practices

- Don't operate at the limit.
- If the `X-Ratelimit-Remaining` is approaching zero, start to slow down.
- Spread requests over time rather than bursting constantly.
- If you need to burst, that is fine; just not every window-size.
- Use staggered scheduling for periodic requests when possible. Ideally not `*/5` cronjobs. But rather: 5 minutes after the last job was finished.
- Respect cache times to minimize unnecessary requests.

## Tentative grouping

| Method | Path | Group |
|--------|------|-------|
| GET | /alliances/ | alliance |
| GET | /alliances/{alliance_id}/ | alliance |
| GET | /alliances/{alliance_id}/corporations/ | alliance |
| GET | /alliances/{alliance_id}/contacts/ | alliance-social |
| GET | /alliances/{alliance_id}/contacts/labels/ | alliance-social |
| GET | /universe/structures/{structure_id}/ | char-asset |
| GET | /characters/{character_id}/assets/ | char-asset |
| POST | /characters/{character_id}/assets/locations/ | char-asset |
| POST | /characters/{character_id}/assets/names/ | char-asset |
| GET | /characters/{character_id}/contracts/ | char-contract |
| GET | /characters/{character_id}/contracts/{contract_id}/bids/ | char-contract |
| GET | /characters/{character_id}/contracts/{contract_id}/items/ | char-contract |
| POST | /characters/{character_id}/cspa/ | char-detail |
| GET | /characters/{character_id}/search/ | char-detail |
| GET | /characters/{character_id}/attributes/ | char-detail |
| GET | /characters/{character_id}/implants/ | char-detail |
| GET | /characters/{character_id}/medals/ | char-detail |
| GET | /characters/{character_id}/portrait/ | char-detail |
| GET | /characters/{character_id}/roles/ | char-detail |
| GET | /characters/{character_id}/skillqueue/ | char-detail |
| GET | /characters/{character_id}/skills/ | char-detail |
| GET | /characters/{character_id}/titles/ | char-detail |
| GET | /characters/{character_id}/agents_research/ | char-industry |
| GET | /characters/{character_id}/blueprints/ | char-industry |
| GET | /characters/{character_id}/industry/jobs/ | char-industry |
| GET | /characters/{character_id}/mining/ | char-industry |
| GET | /characters/{character_id}/planets/ | char-industry |
| GET | /characters/{character_id}/planets/{planet_id}/ | char-industry |
| GET | /characters/{character_id}/clones/ | char-location |
| GET | /characters/{character_id}/fatigue/ | char-location |
| GET | /characters/{character_id}/location/ | char-location |
| GET | /characters/{character_id}/online/ | char-location |
| GET | /characters/{character_id}/ship/ | char-location |
| GET | /markets/structures/{structure_id}/ | char-market |
| GET | /characters/{character_id}/orders/ | char-market |
| GET | /characters/{character_id}/orders/history/ | char-market |
| GET | /characters/{character_id}/calendar/ | char-social |
| GET | /characters/{character_id}/calendar/{event_id}/ | char-social |
| GET | /characters/{character_id}/calendar/{event_id}/attendees/ | char-social |
| GET | /characters/{character_id}/contacts/ | char-social |
| GET | /characters/{character_id}/contacts/labels/ | char-social |
| GET | /characters/{character_id}/mail/ | char-social |
| GET | /characters/{character_id}/mail/{mail_id}/ | char-social |
| GET | /characters/{character_id}/mail/labels/ | char-social |
| GET | /characters/{character_id}/mail/lists/ | char-social |
| GET | /characters/{character_id}/mail/unread/ | char-social |
| GET | /characters/{character_id}/notifications/contacts/ | char-social |
| GET | /characters/{character_id}/standings/ | char-social |
| PUT | /characters/{character_id}/calendar/{event_id}/ | char-social |
| DELETE | /characters/{character_id}/contacts/ | char-social |
| POST | /characters/{character_id}/contacts/ | char-social |
| PUT | /characters/{character_id}/contacts/ | char-social |
| POST | /characters/{character_id}/mail/ | char-social |
| DELETE | /characters/{character_id}/mail/{mail_id}/ | char-social |
| PUT | /characters/{character_id}/mail/{mail_id}/ | char-social |
| POST | /characters/{character_id}/mail/labels/ | char-social |
| DELETE | /characters/{character_id}/mail/labels/{label_id}/ | char-social |
| GET | /characters/{character_id}/loyalty/points/ | char-wallet |
| GET | /characters/{character_id}/wallet/ | char-wallet |
| GET | /characters/{character_id}/wallet/journal/ | char-wallet |
| GET | /characters/{character_id}/wallet/transactions/ | char-wallet |
| GET | /characters/{character_id}/ | character |
| GET | /characters/{character_id}/corporationhistory/ | character |
| POST | /characters/affiliation/ | character |
| GET | /contracts/public/{region_id}/ | contract |
| GET | /contracts/public/bids/{contract_id}/ | contract |
| GET | /contracts/public/items/{contract_id}/ | contract |
| GET | /corporations/{corporation_id}/assets/ | corp-asset |
| POST | /corporations/{corporation_id}/assets/locations/ | corp-asset |
| POST | /corporations/{corporation_id}/assets/names/ | corp-asset |
| GET | /corporations/{corporation_id}/containers/logs/ | corp-asset |
| GET | /corporations/{corporation_id}/facilities/ | corp-asset |
| GET | /corporations/{corporation_id}/starbases/ | corp-asset |
| GET | /corporations/{corporation_id}/starbases/{starbase_id}/ | corp-asset |
| GET | /corporations/{corporation_id}/structures/ | corp-asset |
| GET | /corporations/{corporation_id}/contracts/ | corp-contract |
| GET | /corporations/{corporation_id}/contracts/{contract_id}/bids/ | corp-contract |
| GET | /corporations/{corporation_id}/contracts/{contract_id}/items/ | corp-contract |
| GET | /corporations/{corporation_id}/medals/ | corp-detail |
| GET | /corporations/{corporation_id}/medals/issued/ | corp-detail |
| GET | /corporations/{corporation_id}/shareholders/ | corp-detail |
| GET | /corporations/{corporation_id}/titles/ | corp-detail |
| GET | /corporation/{corporation_id}/mining/extractions/ | corp-industry |
| GET | /corporation/{corporation_id}/mining/observers/ | corp-industry |
| GET | /corporation/{corporation_id}/mining/observers/{observer_id}/ | corp-industry |
| GET | /corporations/{corporation_id}/blueprints/ | corp-industry |
| GET | /corporations/{corporation_id}/customs_offices/ | corp-industry |
| GET | /corporations/{corporation_id}/industry/jobs/ | corp-industry |
| GET | /corporations/{corporation_id}/orders/ | corp-market |
| GET | /corporations/{corporation_id}/orders/history/ | corp-market |
| GET | /corporations/{corporation_id}/members/ | corp-member |
| GET | /corporations/{corporation_id}/members/limit/ | corp-member |
| GET | /corporations/{corporation_id}/members/titles/ | corp-member |
| GET | /corporations/{corporation_id}/membertracking/ | corp-member |
| GET | /corporations/{corporation_id}/roles/ | corp-member |
| GET | /corporations/{corporation_id}/roles/history/ | corp-member |
| GET | /corporations/{corporation_id}/standings/ | corp-member |
| GET | /corporations/{corporation_id}/contacts/ | corp-social |
| GET | /corporations/{corporation_id}/contacts/labels/ | corp-social |
| GET | /corporations/{corporation_id}/divisions/ | corp-wallet |
| GET | /corporations/{corporation_id}/wallets/ | corp-wallet |
| GET | /corporations/{corporation_id}/wallets/{division}/journal/ | corp-wallet |
| GET | /corporations/{corporation_id}/wallets/{division}/transactions/ | corp-wallet |
| GET | /corporations/{corporation_id}/ | corporation |
| GET | /corporations/{corporation_id}/alliancehistory/ | corporation |
| GET | /fw/leaderboards/ | factional-warfare |
| GET | /fw/leaderboards/characters/ | factional-warfare |
| GET | /fw/leaderboards/corporations/ | factional-warfare |
| GET | /fw/stats/ | factional-warfare |
| GET | /fw/systems/ | factional-warfare |
| GET | /fw/wars/ | factional-warfare |
| GET | /characters/{character_id}/fw/stats/ | factional-warfare |
| GET | /corporations/{corporation_id}/fw/stats/ | factional-warfare |
| GET | /characters/{character_id}/fittings/ | fitting |
| POST | /characters/{character_id}/fittings/ | fitting |
| DELETE | /characters/{character_id}/fittings/{fitting_id}/ | fitting |
| GET | /characters/{character_id}/fleet/ | fleet |
| GET | /fleets/{fleet_id}/ | fleet |
| GET | /fleets/{fleet_id}/members/ | fleet |
| GET | /fleets/{fleet_id}/wings/ | fleet |
| PUT | /fleets/{fleet_id}/ | fleet |
| POST | /fleets/{fleet_id}/members/ | fleet |
| DELETE | /fleets/{fleet_id}/members/{member_id}/ | fleet |
| PUT | /fleets/{fleet_id}/members/{member_id}/ | fleet |
| DELETE | /fleets/{fleet_id}/squads/{squad_id}/ | fleet |
| PUT | /fleets/{fleet_id}/squads/{squad_id}/ | fleet |
| POST | /fleets/{fleet_id}/wings/ | fleet |
| DELETE | /fleets/{fleet_id}/wings/{wing_id}/ | fleet |
| PUT | /fleets/{fleet_id}/wings/{wing_id}/ | fleet |
| POST | /fleets/{fleet_id}/wings/{wing_id}/squads/ | fleet |
| GET | /incursions/ | incursion |
| GET | /industry/facilities/ | industry |
| GET | /industry/systems/ | industry |
| GET | /insurance/prices/ | insurance |
| GET | /killmails/{killmail_id}/{killmail_hash}/ | killmail |
| GET | /wars/ | killmail |
| GET | /wars/{war_id}/ | killmail |
| GET | /wars/{war_id}/killmails/ | killmail |
| GET | /characters/{character_id}/killmails/recent/ | char-killmail |
| GET | /corporations/{corporation_id}/killmails/recent/ | corp-killmail |
| GET | /markets/{region_id}/history/ | market |
| GET | /markets/{region_id}/orders/ | market |
| GET | /markets/{region_id}/types/ | market |
| GET | /markets/groups/ | market |
| GET | /markets/groups/{market_group_id}/ | market |
| GET | /markets/prices/ | market |
| GET | /characters/{character_id}/notifications/ | notification |
| GET | /route/{origin}/{destination}/ | routes |
| GET | /sovereignty/campaigns/ | sovereignty |
| GET | /sovereignty/map/ | sovereignty |
| GET | /sovereignty/structures/ | sovereignty |
| GET | /alliances/{alliance_id}/icons/ | static-data |
| GET | /corporations/{corporation_id}/icons/ | static-data |
| GET | /corporations/npccorps/ | static-data |
| GET | /dogma/attributes/ | static-data |
| GET | /dogma/attributes/{attribute_id}/ | static-data |
| GET | /dogma/dynamic/items/{type_id}/{item_id}/ | static-data |
| GET | /dogma/effects/ | static-data |
| GET | /dogma/effects/{effect_id}/ | static-data |
| GET | /loyalty/stores/{corporation_id}/offers/ | static-data |
| GET | /universe/ancestries/ | static-data |
| GET | /universe/asteroid_belts/{asteroid_belt_id}/ | static-data |
| GET | /universe/bloodlines/ | static-data |
| GET | /universe/categories/ | static-data |
| GET | /universe/categories/{category_id}/ | static-data |
| GET | /universe/constellations/ | static-data |
| GET | /universe/constellations/{constellation_id}/ | static-data |
| GET | /universe/factions/ | static-data |
| GET | /universe/graphics/ | static-data |
| GET | /universe/graphics/{graphic_id}/ | static-data |
| GET | /universe/groups/ | static-data |
| GET | /universe/groups/{group_id}/ | static-data |
| POST | /universe/ids/ | static-data |
| GET | /universe/moons/{moon_id}/ | static-data |
| POST | /universe/names/ | static-data |
| GET | /universe/planets/{planet_id}/ | static-data |
| GET | /universe/races/ | static-data |
| GET | /universe/regions/ | static-data |
| GET | /universe/regions/{region_id}/ | static-data |
| GET | /universe/schematics/{schematic_id}/ | static-data |
| GET | /universe/stargates/{stargate_id}/ | static-data |
| GET | /universe/stars/{star_id}/ | static-data |
| GET | /universe/stations/{station_id}/ | static-data |
| GET | /universe/structures/ | static-data |
| GET | /universe/system_jumps/ | static-data |
| GET | /universe/system_kills/ | static-data |
| GET | /universe/systems/ | static-data |
| GET | /universe/systems/{system_id}/ | static-data |
| GET | /universe/types/ | static-data |
| GET | /universe/types/{type_id}/ | static-data |
| GET | /status/ | status |
| POST | /ui/openwindow/contract/ | ui |
| POST | /ui/openwindow/marketdetails/ | ui |
| POST | /ui/autopilot/waypoint/ | ui |
| POST | /ui/openwindow/information/ | ui |
| POST | /ui/openwindow/newmail/ | ui |


