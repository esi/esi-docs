---
search:
  exclude: true

title: Capsuleers.IA
type: service
description: Desktop EVE assistant that runs a local, GPU-accelerated language model over a RAG index of EVE knowledge, and answers with cited sources.
maintainer:
  name: TremalJack
  github: WilliamFalci
---

# Capsuleers.IA

![](icon.png)

Capsuleers.IA is a standalone desktop assistant for EVE Online. Ask about skills, fitting,
terminology, PvE missions, wormholes, sovereignty, exploration or industry and it answers
**with the sources it used**, in English or Italian (auto-detected).

It runs **entirely on your machine**: a local language model, via `node-llama-cpp`, answers
over a retrieval-augmented index of EVE knowledge. Nothing you ask leaves the computer.
The only network calls are the ones a live-data feature explicitly needs — public EVE APIs.

If you want the clipboard intel features without the language models or the knowledge
index, [Capsuleers.Intel](https://github.com/WilliamFalci/capsuleers.intel) is the same app
with the AI removed, at a fraction of the download size.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/WilliamFalci/capsuleers.ia){ .esi-card-link }
- [:octicons-download-16: __Download__](https://github.com/WilliamFalci/capsuleers.ia/releases/latest){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.com/invite/hdbtSFBGD3){ .esi-card-link }

</div>

## Features

- **Q&A on EVE** — skills, fitting, ships and modules, missions, wormholes, sovereignty,
  anomalies, exploration, incursions, planetary interaction and factional warfare, each
  answer carrying the sources it was drawn from.
- **Fit analysis** — paste an EFT fit and get all-V validation (CPU, powergrid, slots,
  hardpoints, drone bandwidth) plus DPS, weapon ranges, EHP and per-layer resistances,
  active and passive tank, capacitor stability, navigation and targeting. The numbers are
  computed **offline** by the Pyfa-parity
  [`eve-fit-engine`](https://www.npmjs.com/package/eve-fit-engine), so no fit is ever sent
  to a server.
- **Pilot intel** — killboard statistics for a pilot, corporation or alliance, with
  leadership and system activity resolved through official **ESI**. When a name matches
  more than one kind of entity, the app asks which one you meant instead of guessing.
- **PvP analytics** — who flies with whom, who hunts whom, recent battles, current
  doctrines, most expensive kills, and killmail forensics.
- **Clipboard intel** — copy a Local roster or a directional scan and get an instant
  read: per-pilot danger flags for the first, an offline ship-class composition for the
  second. Either can be shared as a 24-hour link on
  [capsuleers.app](https://capsuleers.app).
- **Live prices** and **Thera/Turnur connections** — item prices from EVE Ref, wormhole
  connections with entry and exit signatures from EVE-Scout.
- **Model management** — pick, download or delete chat models from an updatable catalogue,
  filtered to a sensible VRAM range for your card.
- **Self-updating knowledge base** — daily jobs track the upstream sources and re-index
  when they change, so the assistant does not drift from the live game.

## Installing

Installers are on the [Releases](https://github.com/WilliamFalci/capsuleers.ia/releases/latest)
page, one per GPU backend: **CUDA** for NVIDIA cards, **Vulkan** for AMD and Intel. Both
fall back gracefully when the preferred backend is unavailable.

The installer itself is lite — code only. On first launch the app downloads, once, the
embedding model, the knowledge index, and a chat model of your choice. There is no macOS
build yet (it needs Apple notarisation), though it builds from source on macOS.

## Licence

Source code is MIT. The bundled and downloaded third-party material — language models,
knowledge sources, static game data — is governed by its own terms, listed in
`THIRD_PARTY.md`. Static game data is used under the EVE Online Developer License
Agreement. Capsuleers.IA is an unofficial, non-commercial fan project.
