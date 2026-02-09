---
search:
  exclude: true

title: OpenClaw EVE ESI Skill
type: service
description: OpenClaw skill for ESI account management with natural language queries, alerts, reports, and market tracking.
maintainer:
  name: burnshall-ui
  github: burnshall-ui
---

# OpenClaw EVE ESI Skill

An [OpenClaw](https://github.com/openclaw/openclaw) skill for interacting with the [EVE Online ESI API](https://developers.eveonline.com/api-explorer) via natural language. Query your characters, receive alerts, generate reports, and track market prices - all through your favorite messaging platform.

<div class="grid cards" markdown>

- [:octicons-browser-16: __ClawHub__](https://clawhub.ai/burnshall-ui/eve-esi){ .esi-card-link }
- [:octicons-mark-github-16: __GitHub__](https://github.com/burnshall-ui/openclaw-eve-skill){ .esi-card-link }

</div>

## Features

- **Natural Language Queries**: Ask questions like "Wie viel ISK habe ich?" or "Show my skill queue"
- **Automated Alerts**: Get notified about war declarations, structure attacks, skill completion, PI extractors, wallet changes, and more
- **Scheduled Reports**: Receive daily/weekly summaries of net worth, skill queue, industry jobs, market orders, and assets
- **Market Tracking**: Monitor prices with customizable thresholds and trend detection for items like PLEX, Skill Injectors, and more
- **Secure Token Handling**: Store tokens via environment variables, never in plain text
- **Config Validation**: Built-in validator checks your configuration and ESI scope coverage
- **Multi-Platform**: Works with Telegram, Discord, Signal, and other OpenClaw-supported platforms

## Installation

```bash
openclaw skill install burnshall-ui/eve-esi
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) installed
- EVE Online SSO application with appropriate scopes
- Python 3.8+ (for bundled scripts)

## Documentation

The skill includes comprehensive documentation for:
- EVE SSO OAuth2 authentication flow
- All available ESI endpoints
- Dashboard configuration (alerts, reports, market tracking)
- JSON Schema for config validation
