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

!!! warning

    For routes that do not have this new rate limiting enabled, there is still an older "error rate limit" active.
    This allows at most 100 non-2xx/3xx responses per minute. After that, it will return 420s on all ESI routes, even those with the new rate limiting enabled.
    The headers described in this document are mutually exclusive to those described in the Error Limit documentation found under "Best Practices".

!!! important

    Some routes also have a rate limiter deep in EVE Server code.
    This can also cause 429s to be returned, without the rate limiter headers indicating why.
    We are working on deprecating these, but in the mean time, be aware this can be the case.

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

| Status Code | Token Cost | Reasoning                                                        |
|-------------|------------|------------------------------------------------------------------|
| 2XX         | 2 tokens   |                                                                  |
| 3XX         | 1 token    | Promote the use of `If-Modified-Since` and `If-Match`.           |
| 4XX         | 5 tokens   | Discourage hitting user-errors. Does not apply to 429 responses. |
| 5XX         | 0 tokens   | You shouldn't be penalized for server-side errors.               |

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
