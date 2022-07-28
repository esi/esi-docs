# ESI (EVE Swagger Interface)
The ESI API is the official RESTful API for EVE third party development. It leverages [Swagger](https://swagger.io/) so that documentation
about the API is always up to date and not dependent on documentation websites like this one. You can find all the endpoints
and try them out at [https://esi.evetech.net/ui/](https://esi.evetech.net/ui/).

## Fundamentals
### Multi-tenant to the core

ESI was designed to be a single interface to all information EVE related. As such, if ESI and the cluster agree on configuration,
you can change the datasource query parameter on any route (including /<version>/swagger.json) to the server name of your choice.

You will see this in the ESI UI as a select menu in the header/nav bar, and in the datasource enum in the spec itself.

There are actually three ESI environments running, an esi-dev, esi-test, and the production esi. With esi-dev or esi-test and a
bit of configuration (which will be replaced with tooling), EVE developers can actually query their local development server through ESI.

### Authentication

Auth is still handled by SSO. There are new scopes which ESI uses, you can make new developer keys (or alter your existing)
to make use of the new scopes. If an ESI endpoint requires authentication, you will see a gray lock icon on the route description in the
Swagger UI. Mouse hovering over this icon will tell you what scope the endpoint requires.

ESI handles redirecting your authentication header to the correct SSO for verification (depending on the datasource query string argument).
SSO is not multi-tenant though, so you will need to create app keys on each SSO backend you intend to use.

### Versioning

ESI itself has an API version (as defined in the spec). That version number is mostly irrelevant to API consumers (it's the version of ESI-lib).
Instead, ESI versions each route individually. This allows us to make much faster changes and avoid the awkward situation of global API versioning.

As an example, let's say you have a route /v1/hello/\<string\>/, and you want to change the path parameter to accepting an integer instead.
With a traditional API, the entire APIs basePath would have to be bumped. This is obviously a little less than ideal, considering there could be hundreds of other unchanged routes.

With ESI, you always (and only) get three complete APIs, /dev/, /latest/ and /legacy/. But each route is also given a numbered path, starting with /v1/.
Alternate routes are mentioned in the route description (until something better comes along in the standards?).

/dev/ can change at any point, changes to /latest/ will be announced. After changes are made the previous /latest/ will be available as /legacy/, until the next version bump.
If you want to avoid the return schema of your request suddenly changing, you can use the versioned alternate route. In that case, prudent developers may want to
create unit tests (watch for the `warning: 199` headers) to notify them when endpoints are moved to legacy.

Additionally, endpoints may be deprecated. When an endpoint is deprecated, a line appears through it on the Swagger UI, and it begins returning the "warning: 299" header.
This is slightly different than a `warning: 199` header, which you will receive if an endpoint was updated and there is now a newer version of it available.
Deprecation is how Tech Co broadcasts an intent to delete a route. Deprecated endpoints may include a recommended alternate source or
other message in the 299 warning, and you should move away from them immediately.

Because endpoints are versioned individually, the concept of an overall /v1/ (or 2 or 5) API is not very relevant, and no swagger-ui is provided for these routes.
Browsing the API's capabilities should be done via /dev/, /latest/ or /legacy/. However, users who wish to indulge their curiosity may feed a
/v1/swagger.json into their own Swagger UI to get an overview, if they wish.

As an aside, all ESI routes end with a /. The only exceptions are the /\<version\>/swagger.json routes and routes used by the swagger-ui, which are passed through ESI.

## Rules

#### Error Limit

ESI limits how many errors you're allowed to get within a set time frame. The details are explained in the ESI dev blog: [Error Rate Limiting](https://developers.eveonline.com/blog/article/error-limiting-imminent)  
Once you reach the error limit, all your request are automatically discarded until the end of the time frame.  
Failing to respect the error limit can get you banned from ESI.  
This system allows ESI to not use a fixed request rate limit.
  
Error limit headers:  
`X-ESI-Error-Limit-Remain` errors left in this time frame.  
`X-ESI-Error-Limit-Reset` seconds left until next time frame and errors reset to zero.
  
#### Caching
The `expires` header represent when new data will be available. You should not update before that.  
If you update before, the best case scenario is that you will get a cached result, wasting resources on both side of the request.  
In the worst case scenario you will get new data and it may count as circumventing the ESI caching.  
Circumventing the ESI caching can get you banned from ESI.

Cache headers:  
`expires` when new data is available.  
`last-modified` when the data was last updated

#### Discovery
You're not allowed to use ESI to discover structures/characters/etc.  
That includes the search endpoints, but, is not limited to those endpoints.  
Abusing any endpoint for discovery can get you banned from ESI.  
See: [The ESI API is a shared resource, do not abuse it](https://developers.eveonline.com/blog/article/the-esi-api-is-a-shared-resource-do-not-abuse-it)  

#### Rate Limit
Some endpoints, specifically for sending mail and reading contracts, have internal rate limits enforced by the EVE monolith. If these rate limits are exceeded, ESI will return HTTP status code 520. More info in the ESI issue: [Error 520](https://github.com/esi/esi-issues/issues/636)  
The 520 error is counted in the error limit.

#### Spread Load
ESI is a shared resource and projects should be optimized to have minimum consumption of unnecessary resources. In the case of long running
services, consistent amounts of slow traffic are preferred to spiky, high throughput traffic.

#### Historic Data
You can get banned for high load on endpoints with historic data (killmails/wars/others?). There are no specifications about what constitute high load, that is entirely up to CCP to decide as needed. Killmails are usually safe with less than 50 rps (requests per second), but, there are no guarantees - this isn't official CCP policy, it's simple advice from another 3rd party developer.

#### User Agent
When making requests, it's recommended you set a `User-Agent` header in your client which includes the source of the request and contact information. This way, CCP can identify and help you with issues if you're banned.

#### IP Ban Avoidance
If you're banned from the ESI, this ban will be a permanent ban based on your IP. It's recommended that you reach out to CCP to resolve the ban and do not try to avoid the ban by changing your IP.
