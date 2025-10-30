---
search:
  exclude: true

title: elt
type: service
description: elt is a command line tool for looking up Eve Online objects. It's available for Windows, macOS and Linux.
maintainer:
  name: Erik Kalkoken
  github: ErikKalkoken
---

# elt - EVE Lookup Tool

**elt** is a command line tool for looking up Eve Online objects. It's available for Windows, macOS and Linux.

[![GitHub Release](https://img.shields.io/github/v/release/ErikKalkoken/elt)](https://github.com/ErikKalkoken/elt/elt)
[![GitHub License](https://img.shields.io/github/license/ErikKalkoken/elt)](https://github.com/ErikKalkoken/elt?tab=MIT-1-ov-file#readme)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/tVSCQEVJnJ)

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/ErikKalkoken/elt){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.gg/tVSCQEVJnJ){ .esi-card-link }

</div>

**elt** is a command line tool that looks up EVE Online objects from the game server and prints them in the terminal. It provides a convenient and fast alternative to using a browser or curl commands for quickly resolving Eve IDs or names in the terminal.

For example:

```sh
elt "Jita"
```

Will print

```plain
Solar System:
┌──────────┬──────┬──────────────────┬────────────────────┬───────────┬─────────────┬────────────┐
│    ID    │ NAME │ CONSTELLATION ID │ CONSTELLATION NAME │ REGION ID │ REGION NAME │  SECURITY  │
├──────────┼──────┼──────────────────┼────────────────────┼───────────┼─────────────┼────────────┤
│ 30000142 │ Jita │ 20000020         │ Kimotoro           │ 10000002  │ The Forge   │ 0.94591314 │
└──────────┴──────┴──────────────────┴────────────────────┴───────────┴─────────────┴────────────┘
```

For more information please visit the [Github repository](https://github.com/ErikKalkoken/elt).
