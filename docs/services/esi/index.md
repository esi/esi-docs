---
title: ESI
---
# EVE Swagger Interface (ESI)

The ESI API is the official RESTful API for EVE third-party development. You can find all the endpoints and try them out in the [Swagger UI interface](https://esi.evetech.net/ui/).

## Authentication

While some ESI endpoints are public, many require authentication, which is handled by [SSO](../sso/). If an ESI endpoint requires authentication, you will see a grey lock icon on the route description in the Swagger UI. The route description lists the required scopes.

## Versioning

ESI versions each route individually. You always get three complete APIs, `/dev/`, `/latest/` and `/legacy/`. But each route is also given a numbered path, starting with `/v1/`. Alternate routes are mentioned in the route description.

`/dev/` can change at any point, changes to `/latest/` will be announced. After changes are made the previous `/latest/` will be available as `/legacy/`, until the next version bump. If you want to avoid the schema of your request suddenly changing, use the versioned alternate route. In that case, prudent developers may want to watch for `warning: 199` headers to notify them when endpoints are moved to legacy.

Endpoints may become deprecated. When an endpoint is deprecated, a strikethrough line appears through it on the Swagger UI, and it begins returning the `warning: 299` header. This is slightly different from a `warning: 199` header, which you will receive if an endpoint was updated and there is now a newer version of it available. Deprecation is how intent to delete a route is broadcasted. Deprecated endpoints may include a recommended alternate source or other message in the 299 warning, and you should move away from them immediately.

## Best Practices for ESI

The following are some best practices when you interact with ESI. Not all are hard requirements, but they are highly recommended to ensure a smooth experience for both you and CCP. Remember that the ESI API is a shared resource, do not abuse it.

### User Agents

All ESI requests **should** contain User Agent information indicating the application making the request. This information can be used by CCP to identify the source of requests, and in some cases, to contact the developers if there are issues with the application.

It should be noted that for browser applications, you may not be able to set the `User-Agent` header directly [1]. In this case, you should use the `X-User-Agent` header instead. If neither of these options is available, you can use the `user_agent` query parameter [2].

A simple flowchart to help you decide how to send your user agent information:

{% raw %}
``` mermaid
flowchart LR
    Q1{{Can you set HTTP headers?}}
    Q2{{Is your app a browser application?}}
    A1[Use 'User-Agent' Header]
    A2["Use 'X-User-Agent' Header [1]"]
    A3["Use 'user_agent' Query Parameter [2]"]
    Q1 -->|Yes| Q2
    Q1 -->|No| A3
    Q2 -->|Yes| A2
    Q2 -->|No| A1
```
{% endraw %}

!!! note "[1] `User-Agent` vs `X-User-Agent` Header"

    The `User-Agent` header used to be [forbidden](https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_request_header), but no longer is. However, Chrome and Chromium-based browsers still silently drop the header from Fetch requests. This is why we recommend using `X-User-Agent` for browser applications instead.

!!! note "[2] `user_agent` Query Parameter"

    If you are unable to set request headers, you can use the `user_agent` query parameter to still send your user agent information. Keep in mind that like any other query parameter, this will need to be URL-encoded.

#### Information to transmit

The User Agent information you send should contain one or more of the following :

- An Email Address (**Strongly Preferred**) `(foo@example.com)`
- App Name with version (**Strongly Preferred**) `AppName/1.2.3`
- A URL to Source Code `(+https://github.com/your/repository)`
- A Discord Username `(discord:username)`
- An EVE Character `(eve:charactername)`

While User Agents are not a defined web standard, the MDN provides a thoroughly documented set of examples <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent>; following these standards will ensure your useragent is well understood.

#### Libraries/frameworks

If your application consists of multiple _products_ such as an upstream library, or if you are a plugin/extension of a larger app, you may like to list these in _narrow to broad_ order, with your useragent being more to less precise. You should _always_ include the source of the code generating the request.

```text
PluginName/1.2.3 (foo@example.com; +https://github.com/) AppName/1.2.3 LibraryName/1.2.3
```

#### Examples

```
AllianceAuth/1.2.3 (foo@example.com; +https://gitlab.com/allianceauth/allianceauth) DjangoESI/1.2.3
AASRP/1.2.3 (foo@example.comm; +https://github.com/ppfeufer/aa-srp) DjangoESI/1.2.3
eveseat:eveapi/5.0.22 (admin contact: foo@example) (https://github.com/eveseat/seat) eveseat:seat/5.0.x-dev eveseat:web/5.0.23 eveseat:eveapi/5.0.22
RIFT/1.2.3 (foo@example.com)
```

### Error Limit

ESI limits how many errors you’re allowed to get within a set time frame. Once you reach the error limit, all your request are automatically discarded until the end of the time frame. Failing to respect the error limit can get you banned from ESI. This system allows ESI to not use a fixed request rate limit.

Error limit headers:  
`X-ESI-Error-Limit-Remain` errors left in this time frame.  
`X-ESI-Error-Limit-Reset` seconds left until next time frame and errors reset to zero.

The details are explained in this blog post: [Error Rate Limiting](/blog/error-rate-limiting-imminent)

### Caching

The ESI acts as both an http handler for resources available in the monolith, and a cache manager of those resources' representation. You can get a benefit from the caching in several ways, depending on the request you send.

The `expires` header represents when the resource cache in ESI should expire, that is when updated data should be available.
You should not update before that. If you update before, the best case scenario is that you will get a cached result, wasting resources on both side of the request. In the worst case scenario you will get new data, and it may count as circumventing the ESI caching. Circumventing the ESI caching can get you banned from ESI.

The `last-modified` header indicates when the data was last updated in the cache.

The `ETag` header is a hash of the content. Once you have received that header with a response, in a subsequent request you can add the `If-None-Match` header set to the last retrieved value. If the data did not change since the last cached value, the server will return a `304` response code instead of e.g. `200`, meaning there is no change to handle.

Notes: 
 - When requesting a paginated resource, each of those headers should be the same for all the pages of a single resource. Checking this constraint allows you to validate the data retrieved, typically by avoiding the case where the data is refreshed between the calls to two different pages. This can also happen outside of ESI cache refresh.
 - Some resources may not provide such headers, typically POST methods can have no cache information, while still actually having internal cache.
 - Static data should have the same shared caching information. That is, planets, moons, types etc. path should return the same caching headers.

## Support

ESI has its own issues repository at [esi-issues](https://github.com/esi/esi-issues). From there you can raise issues or ask for new features. Also see the general [support page](../../support/).

### ESI Bans

If you have been banned from ESI, responses to your requests will point you to the EVE Online support system. Please follow the instructions. Circumventing the ban can result in further action being taken, up to and including a permanent ban for all of your accounts.
