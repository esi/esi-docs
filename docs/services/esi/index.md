---
title: ESI
---
# EVE Swagger Interface (ESI)

## User-Agent

All ESI Requests should be accompanied by an appropriate User-Agent request header providing a method for CCP to contact the source of the request in the event of an issue.

This could be one or more of the following

- An EVE Character
- An Email Address
- A Discord UID
- An App Name

### Best Practice

While User Agents are not a defined web standard, the MDN provides a thoroughly documented set of examples <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent>, Following these standards will ensure your useragent is well understood.

`AppName/0.0.0 email@address.com`

If your application consists of multiple _products_ such as an upstream library, or if you are a plugin/extension of a larger app, you may like to list these in _narrow to broad_ order, with your useragent being more to less precise. You should _always_ include the source of the code generating the request.

`PluginName/0.0.0 AppName/0.0.0 LibraryName/0.0.0 email@address.com`

You may, if you choose, include some additional information to identify your app such as a Git URL in the bracketed comment

`PluginName/0.0.0 (+https://github.com/) AppName/0.0.0 LibraryName/0.0.0 email@address.com`
