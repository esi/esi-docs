---
title: Overview
---
# EVE Swagger Interface (ESI)

The ESI API is the official RESTful API for EVE third-party development. You can find all the endpoints and try them out in the [Swagger UI interface](https://esi.evetech.net/ui/). Some endpoints have additional details on [this page](../endpoints/).

## Authentication

While some ESI endpoints are public, many require authentication, which is handled by [SSO](../../sso/). If an ESI endpoint requires authentication, you will see a grey lock icon on the route description in the Swagger UI. The route description lists the required scopes.

## Versioning

ESI versions each route individually. You always get three complete APIs, `/dev/`, `/latest/` and `/legacy/`. But each route is also given a numbered path, starting with `/v1/`. Alternate routes are mentioned in the route description.

`/dev/` can change at any point, changes to `/latest/` will be announced. After changes are made the previous `/latest/` will be available as `/legacy/`, until the next version bump. If you want to avoid the schema of your request suddenly changing, use the versioned alternate route. In that case, prudent developers may want to watch for `warning: 199` headers to notify them when endpoints are moved to legacy.

Endpoints may become deprecated. When an endpoint is deprecated, a strikethrough line appears through it on the Swagger UI, and it begins returning the `warning: 299` header. This is slightly different from a `warning: 199` header, which you will receive if an endpoint was updated and there is now a newer version of it available. Deprecation is how intent to delete a route is broadcasted. Deprecated endpoints may include a recommended alternate source or other message in the 299 warning, and you should move away from them immediately.

## Support

ESI has its own issues repository at [esi-issues](https://github.com/esi/esi-issues). From there you can raise issues or ask for new features. Also see the general [support page](../../../support/).

## ESI Bans

If you have been banned from ESI, responses to your requests will point you to the EVE Online support system. Please follow the instructions. Circumventing the ban can result in further action being taken, up to and including a permanent ban for all of your accounts.
