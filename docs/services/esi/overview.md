---
title: Overview
---
# EVE Swagger Interface (ESI)

The ESI API is the official RESTful API for EVE third-party development. You can find all the endpoints and try them out in the [Swagger UI interface](https://esi.evetech.net/ui/). Some endpoints have additional details on [this page](../endpoints/).

## Authentication

While some ESI endpoints are public, many require authentication, which is handled by [SSO](../../sso/). If an ESI endpoint requires authentication, you will see a grey lock icon on the route description in the Swagger UI. The route description lists the required scopes.

## Versioning

Every ESI request can include an `X-Compatibility-Date` header using the ISO format - `YYYY-MM-DD`. This header tells ESI "This application was built or updated at this date - give me the API behavior as it was at that date". If applications cannot set custom headers, the `compatibility_date` query parameter will do the same.
The date cannot be in the future, neither can it below a minimum threshold (the "oldest" versions available). If this minimum bar is raised, this will be clearly communicated via dev-blogs.

The API changes date at 11:00 UTC.
So if you want to use the date of today, use (pseudo-code): `now() - 11 * 60 * 60`, to get the current date of the API.

### Breaking changes

Any breaking changes will be released under a new `X-Compatibility-Date`. Breaking changes include:

- Removing of request parameters.
- Removing of response fields / response headers / enum values.
- Adding or changing request parameters that are (now) required.
- Changing the type of request parameters / response fields / response headers.

Any non-breaking changes will not introduce a new `X-Compatibility-Date`. Non-breaking changes include:

- Adding of optional request parameters.
- Adding of response fields / response headers / enum values.

## Support

ESI has its own issues repository at [esi-issues](https://github.com/esi/esi-issues). From there you can raise issues or ask for new features. Also see the general [support page](../../../support/).

## ESI Bans

If you have been banned from ESI, responses to your requests will point you to the EVE Online support system. Please follow the instructions. Circumventing the ban can result in further action being taken, up to and including a permanent ban for all of your accounts.
