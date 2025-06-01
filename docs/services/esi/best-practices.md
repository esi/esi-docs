---
title: Best Practices for ESI
---
# Best Practices for ESI

The following are some best practices when you interact with ESI. Not all are hard requirements, but they are highly recommended to ensure a smooth experience for both you and CCP. Remember that the ESI API is a shared resource, do not abuse it.

## User Agents

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

### Information to transmit

The User Agent information you send should contain one or more of the following :

- An Email Address (**Strongly Preferred**) `(foo@example.com)`
- App Name with version (**Strongly Preferred**) `AppName/1.2.3`
- A URL to Source Code `(+https://github.com/your/repository)`
- A Discord Username `(discord:username)`
- An EVE Character `(eve:charactername)`

While User Agents are not a defined web standard, the MDN provides a thoroughly documented set of examples <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent>; following these standards will ensure your useragent is well understood.

### Libraries/frameworks

If your application consists of multiple _products_ such as an upstream library, or if you are a plugin/extension of a larger app, you may like to list these in _narrow to broad_ order, with your useragent being more to less precise. You should _always_ include the source of the code generating the request.

```text
PluginName/1.2.3 (foo@example.com; +https://github.com/) AppName/1.2.3 LibraryName/1.2.3
```

### Examples

```
AllianceAuth/1.2.3 (foo@example.com; +https://gitlab.com/allianceauth/allianceauth) DjangoESI/1.2.3
AASRP/1.2.3 (foo@example.comm; +https://github.com/ppfeufer/aa-srp) DjangoESI/1.2.3
eveseat:eveapi/5.0.22 (admin contact: foo@example) (https://github.com/eveseat/seat) eveseat:seat/5.0.x-dev eveseat:web/5.0.23 eveseat:eveapi/5.0.22
RIFT/1.2.3 (foo@example.com)
```

## Error Limit

ESI limits how many errors you’re allowed to get within a set time frame. Once you reach the error limit, all your request are automatically discarded until the end of the time frame. Failing to respect the error limit can get you banned from ESI. This system allows ESI to not use a fixed request rate limit.

Error limit headers:  
`X-ESI-Error-Limit-Remain` errors left in this time frame.  
`X-ESI-Error-Limit-Reset` seconds left until next time frame and errors reset to zero.

The details are explained in this blog post: [Error Rate Limiting](/blog/error-rate-limiting-imminent)

## Caching

The ESI acts as both an http handler for resources available in the monolith, and a cache manager of those resources' representation. You can get a benefit from the caching in several ways, depending on the request you send.

The `expires` header represents when the resource cache in ESI should expire, that is when updated data should be available.
You should not update before that. If you update before, the best case scenario is that you will get a cached result, wasting resources on both side of the request. In the worst case scenario you will get new data, and it may count as circumventing the ESI caching. Circumventing the ESI caching can get you banned from ESI.

The `last-modified` header indicates when the data was last updated in the cache.

The `ETag` header is a hash of the content. Once you have received that header with a response, in a subsequent request you can add the `If-None-Match` header set to the last retrieved value. If the data did not change since the last cached value, the server will return a `304` response code instead of e.g. `200`, meaning there is no change to handle.

Notes:

- When requesting a paginated resource, the `last-modified` header should be the same for all the pages of a single resource. Checking this constraint allows you to validate the data retrieved, typically by avoiding the case where the data is refreshed between the calls to two different pages. This issue can also happen outside of ESI cache refresh.
- Some resources may not provide such headers, typically POST methods have no cache information, even when they still actually have an internal cache.
- Static data should have the same shared caching information. That is, planets, moons, types, etc. paths should return the same caching headers.
