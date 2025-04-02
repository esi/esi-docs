---
search:
  exclude: true

title: EVE ESI Proxy
type: resource
description: An HTTP proxy for the ESI API.
maintainer:
  name: Kenneth Jørgensen
  github: autonomouslogic
---

# EVE ESI Proxy

An HTTP proxy specifically designed for the ESI API.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/autonomouslogic/eve-esi-proxy){ .esi-card-link }
- [:simple-discord: __Discord__](https://everef.net/discord){ .esi-card-link }

</div>

## Features

The ESI API is a great resource, but can be difficult to work with.
The features below are all things you have to be acutely aware of.
Using this proxy will let you get on with writing your application and not worry about the minutiae of ESI lore.

* **Character login** is supported and OAuth is handled automatically
* **Cache responses** to disk to improve request times and reduce load on the ESI itself
* **Conditional requests** to refresh objects in the cache
* **Rate limiting** to help avoid being banned, including different limits for the endpoints which have special undocumented limits
* **Handle ESI error limit headers** to stop all requests if the limit is reached
* **Retry failed requests** if a 5xx is returned
* **User agent header** is automatically handled
* **Fetching multiple pages concurrently** if no page (or page 0) is set in the request, merging all pages into a single response

Caching, rate limiting, retries, etc. are all handled transparently.

## Usage
Run via Docker:
```bash
docker run -it -v eve-esi-proxy:/data -p 8182:8182 -m 2g -e "ESI_USER_AGENT=<your email>" autonomouslogic/eve-esi-proxy:latest
```

Then you request data as you would on the ESI, just from localhost instead:
```bash
curl "http://localhost:8182/latest/status/"
```
or
```bash
curl "http://localhost:8182/latest/markets/10000002/orders/?order_type=all"
```