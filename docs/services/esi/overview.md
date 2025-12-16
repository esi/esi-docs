---
title: Overview
---
# EVE Swagger Interface (ESI)

The ESI API is the official RESTful API for EVE third-party development. You can find all the endpoints and try them out in the [API Explorer](/api-explorer). Some endpoints have additional details on [this page](../endpoints/).

## Authentication

While some ESI endpoints are public, many require authentication, which is handled by [SSO](../../sso/). The route descriptions in the API Explorer indicate which endpoints require authentication, and with which scopes.

## Versioning

Every ESI request can include an `X-Compatibility-Date` header using the ISO format - `YYYY-MM-DD`.
This header tells ESI, "This application's ESI implementation was updated or reviewed at this date – give me the API behavior as it was at that date".
If applications cannot set custom headers, the `compatibility_date` query parameter will do the same.
If a request does not set a compatibility date, the oldest available compatibility date is used.

The date cannot be in the future, neither can it below a minimum threshold (the "oldest" versions available).
If this minimum bar is raised, this will be clearly communicated via dev-blogs.

The API changes date at 11:00 UTC.
So if you want to use the date of today, use (pseudocode): `now() - 11 * 60 * 60`, to get the current date of the API.

### New Compatibility Date

The following changes will always be released under a new compatibility date:

- Adding of new routes.
- Adding or changing of (now to be) required request parameters.
- Changing the type of request parameters / response fields / response headers.
- Removing of request parameters.
- Removing of response fields / response headers / enum values.

The following changes will always be released as part of the existing compatibility dates:

- Adding of optional request parameters.
- Adding of response fields / response headers / enum values.

## Support

ESI has its own issues repository at [esi-issues](https://github.com/esi/esi-issues). From there you can raise issues or ask for new features. Also see the general [support page](../../../support/).

## ESI Bans

If you have been banned from ESI, responses to your requests will point you to the EVE Online support system. Please follow the instructions. Circumventing the ban can result in further action being taken, up to and including a permanent ban for all of your accounts.
