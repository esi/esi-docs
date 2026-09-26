---
search:
  exclude: true

title: Capsuleers.Intel
type: service
description: Cross-platform desktop intel tool. Copy your Local roster or a D-Scan and see who you are up against and how the hostile fleet is composed.
maintainer:
  name: TremalJack
  github: WilliamFalci
---

# Capsuleers.Intel

![](icon.png)

Capsuleers.Intel is a standalone desktop app for Windows and Linux. Copy your **Local**
window or a **directional scan** and it tells you, at a glance, who is in system and what
the hostile fleet is flying.

It is the intel-only sibling of [Capsuleers.IA](https://github.com/WilliamFalci/capsuleers.ia): the same
clipboard intel features and the same interface, **without** the local AI assistant, the
language models or the knowledge index — so the download is tens of megabytes instead of
gigabytes, with nothing to set up on first launch.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/WilliamFalci/capsuleers.intel){ .esi-card-link }
- [:octicons-download-16: __Download__](https://github.com/WilliamFalci/capsuleers.intel/releases/latest){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.com/invite/hdbtSFBGD3){ .esi-card-link }

</div>

## Features

- **Local intel** — paste the Local member list and get a per-pilot roster: kills, losses,
  efficiency, a danger rating, archetype tags, and a per-pilot dossier with playstyle,
  frequent wingmates and recently used hulls. A summary strip totals alliances,
  corporations and pilots, and lists every detected alliance as a chip.
- **D-Scan analysis** — paste a D-Scan and get the composition broken down by ship class,
  computed **fully offline** from a bundled SDE snapshot. The system is inferred from the
  celestial names, so it works in any client language.
- **Clipboard watch** — an opt-in background watcher picks up a Local or a D-Scan the
  moment you copy it, with an audible cue, so it keeps working while you play fullscreen
  on another monitor. On Wayland it reads through `wl-paste` so background copies are seen
  even when the app is not focused.
- **Mini mode** — shrink to an always-on-top icon, or minimise to the system tray.
- **Share** — turn any intel or D-Scan into a shareable link (valid 24 hours) on
  [capsuleers.app](https://capsuleers.app), with a history list and a live countdown.

## Privacy

No account, no telemetry. Nothing leaves your machine except the lookups a feature
explicitly needs: pilot names go to a killboard for Local intel, and a raw scan goes to
capsuleers.app **only when you press Share**. D-Scan analysis is entirely offline.

The renderer is sandboxed and context-isolated behind a narrow IPC bridge with a strict
`connect-src 'self'` Content-Security-Policy, and the packaged binary is hardened with
Electron fuses.

## Licence

Source code is MIT. Static game data is used under the EVE Online Developer License
Agreement.
