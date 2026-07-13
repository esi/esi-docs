---
search:
  exclude: true

title: EVE AI Agent
type: service
description: A self-hosted chat-first AI assistant for EVE Online with Telegram and Discord bots, EVE SSO, live ESI data, local SDE search, route planning, and killboard intelligence.
maintainer:
  name: garshany
  github: garshany
---

# EVE AI Agent

EVE AI Agent is a self-hosted chat-first assistant for EVE Online. Run it with Telegram or Discord, or use its terminal CLI. It uses the official EVE SSO and ESI APIs for player-authorized character data, a local SDE SQLite database for static data, and public EVE community data sources for route and combat intelligence.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/garshany/eveai){ .esi-card-link }

</div>

## Features

- Natural-language EVE assistance in Telegram private chats, Discord DMs, or a terminal CLI.
- EVE SSO character linking with encrypted local token storage and scope-aware access to private ESI data.
- Local SDE lookup for systems, items, dogma, blueprints, and routes; live ESI for authorized character, corporation, market, assets, skills, industry, mail, and location data.
- Route planning with danger analysis, killmail context, gate-camp signals, and Thera or Turnur shortcuts.
- D-scan, local and fleet analysis, zKillboard and EVE-KILL intelligence, EVE-Scout data, and opt-in chat notifications.

## Self-hosting

The project is available under the MIT license. See its GitHub README for setup, EVE Developer application configuration, and deployment guidance.
