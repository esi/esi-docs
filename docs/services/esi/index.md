---
title: ESI
---
# EVE Swagger Interface (ESI)

## User-Agent

All ESI Requests should be accompanied by an appropriate User-Agent request header providing a method for CCP to contact the source of the request in the event of an issue.

This could be one or more of the following

- An Email Address (Strongly Preferred)
- An App Name (Strongly Preferred)
- A URL to Source Code
- A Discord UID
- An EVE Character

### Best Practice

While User Agents are not a defined web standard, the MDN provides a thoroughly documented set of examples <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent>, Following these standards will ensure your useragent is well understood.

```text
AppName/1.2.3 (foo@example.com)
```

You may, if you choose, include any additional information to identify your app. Following the MDN standard.

- A URL to your documentation or source code, remembering to prefix `+` on a URL `(+https://github.com/)`
- A Discord Username `(discord:username)`
- An EVE Character `(eve:charactername)`

```text
AppName/1.2.3 (foo@example.com; +https://github.com/)
```

If your application consists of multiple _products_ such as an upstream library, or if you are a plugin/extension of a larger app, you may like to list these in _narrow to broad_ order, with your useragent being more to less precise. You should _always_ include the source of the code generating the request.

```text
PluginName/1.2.3 (foo@example.com; +https://github.com/) AppName/1.2.3 LibraryName/1.2.3
```

#### Examples

A Non-Exhaustive list of examples is provided below, Developers feel free to add your UAs for CCP and our own reference

```text
AllianceAuth/1.2.3 (foo@example.com; +https://gitlab.com/allianceauth/allianceauth) DjangoESI/1.2.3
AASRP/1.2.3 (foo@example.comm; +https://github.com/ppfeufer/aa-srp) DjangoESI/1.2.3
eveseat:eveapi/5.0.22 (admin contact: foo@example) (https://github.com/eveseat/seat) eveseat:seat/5.0.x-dev eveseat:web/5.0.23 eveseat:eveapi/5.0.22
RIFT/1.2.3 (foo@example.com)
```
