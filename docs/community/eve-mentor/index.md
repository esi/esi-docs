---
search:
  exclude: true

title: EVE Mentor
type: service
description: An AI mentor for new and returning pilots — explains your losses, plans your skills, checks your fits, and finds your stranded assets, from live EVE data.
maintainer:
  name: Henry Robinson
  github: henryjrobinson
---

# EVE Mentor

EVE Mentor is a free, open-source AI mentor for new and returning pilots, available
at [https://ruby-eve.com](https://ruby-eve.com). It is an
[MCP](https://modelcontextprotocol.io) server that connects an AI assistant (Claude,
or any MCP client) to live EVE data, so you can ask the questions new players actually
have — *"why do I keep dying?"*, *"what do I need to fly a Vexor?"*,
*"what should I do tonight?"*, *"where did my stuff go?"* — and get answers grounded
in real data instead of guesswork.

<div class="grid cards" markdown>

- [:octicons-browser-16: **Website**](https://ruby-eve.com){ .esi-card-link }
- [:simple-github: **GitHub**](https://github.com/henryjrobinson/eve-mentor-mcp){ .esi-card-link }
- [:simple-npm: **npm**](https://www.npmjs.com/package/eve-mentor-mcp){ .esi-card-link }

</div>

## What it does

EVE Mentor turns live ESI and zKillboard data into plain-language coaching for
someone still learning the game:

- **Loss analysis** — pulls your real losses with full fit detail and explains what went wrong.
- **Skill planning** — "can I fly this ship/fit?" with a training plan diffed against your actual skills.
- **Fitting & combat** — mechanical fit checks, proven fits learned from real killmails, ammo/damage-type advice.
- **Direction & ISK** — a career "sorting hat", income guidance by skillpoint tier, and "what should I do tonight?".
- **Safety & logistics** — per-jump route danger with named gank chokepoints, where to buy across the trade hubs, and newbie-friendliness checks on corps.
- **Returning players** — a "what's happening" briefing and a stranded-asset finder.

## Access and privacy

Public tools work with no login. Character tools use **read-only ESI scopes** over
OAuth2 PKCE — EVE Mentor never modifies anything on your account, and your login stays
on your own machine (no client secret involved). Built under the
[CCP Developer License](https://developers.eveonline.com/license-agreement)
(non-commercial); not affiliated with or endorsed by CCP hf.
