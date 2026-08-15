---
search:
  exclude: true

title: OpenClaw EVE ESI Skill
type: service
description: An OpenClaw agent skill that answers questions about your characters in natural language, with read-only ESI access by default and tokens kept on your own machine.
maintainer:
  name: burnshall-ui
  github: burnshall-ui
---

# OpenClaw EVE ESI Skill

A skill for [OpenClaw](https://openclaw.ai) that lets a self-hosted agent answer
questions about your EVE characters in plain language — "how much ISK do I
have", "what is my skill queue", "which extractors run out tonight". It talks to
the official EVE SSO and ESI APIs only; there is no intermediate service, and
your tokens never leave the machine you run it on.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/burnshall-ui/openclaw-eve-skill){ .esi-card-link }
- [:octicons-browser-16: __ClawHub__](https://clawhub.ai/burnshall-ui/skills/eve-esi){ .esi-card-link }

</div>

## Features

- Natural-language queries against character, corporation and universe data —
  wallet, assets, skills, clones, location, industry, contracts and market.
- Planetary Interaction reporting: extractor timers, storage fill levels and
  attention flags across every colony on a character.
- Market price lookups, including the live Jita order book for a given type.
- Threat assessment and route planning from ESI kill, jump, faction-warfare and
  incursion data.
- A validated JSON Schema vocabulary for describing alerts, reports and price
  thresholds, so an agent's own automation has a well-defined config to act on.
  The skill validates such a config and checks it against the granted scopes; it
  does not itself poll, schedule or deliver notifications.
- Read-only by default: any state-changing request is refused unless the
  operator explicitly passes `--allow-write`.

## ESI usage

- Requests go to `https://esi.evetech.net` with no version prefix and carry an
  `X-Compatibility-Date` header pinned to a reviewed date, rather than relying
  on the oldest supported behaviour.
- Every ESI and SSO request sends a `User-Agent` naming the skill, its version
  and this repository; operators can add a contact address via an environment
  variable.
- `429` responses are retried after `Retry-After` and `420` after the
  error-limit reset, with a bounded retry budget. Cache expiry is surfaced to
  the caller rather than worked around.

## Authentication and scopes

Login uses EVE SSO with OAuth2 and PKCE, so there is no client secret to leak.
Tokens are written to a `chmod 600` file on the operator's own machine and
refreshed in-process; the skill is built so that a token never has to appear on
a command line or in a log.

Scopes are requested by profile rather than all at once — the default profile
asks for eight read scopes, and wallet and mail are only included if the
operator explicitly chooses the widest profile. The flow prints the exact scope
list before opening the browser.

## Self-hosting

MIT licensed, Python standard library only, no pip dependencies. Requires an
OpenClaw installation and an EVE Developer application for the Client ID. See
the GitHub README for setup and configuration.
