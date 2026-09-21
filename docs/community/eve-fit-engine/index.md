---
search:
  exclude: true

title: eve-fit-engine
type: resource
description: Pyfa-parity ship and Upwell-structure fitting calculation engine for JavaScript. Give it a fit, get the full derived stat block.
maintainer:
  name: TremalJack
  github: WilliamFalci
---

# eve-fit-engine

`eve-fit-engine` is an npm package that computes the derived stat block of an EVE Online
ship or Upwell structure fit: offense (DPS, alpha, application), defense (EHP, resists,
active and passive tank), capacitor (stability and simulation), navigation, targeting,
fitting (CPU / powergrid / calibration), projected effects, and structure fuel and
service stats.

It is the calculation engine behind [Capsuleers.app](https://capsuleers.app), extracted
so that other developers can build fitting tools without reimplementing dogma.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/WilliamFalci/capsuleers.fitting-engine){ .esi-card-link }
- [:simple-npm: __npm__](https://www.npmjs.com/package/eve-fit-engine){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.com/invite/hdbtSFBGD3){ .esi-card-link }

</div>

## Two entry points

- **Base (`eve-fit-engine`)** — framework-free. No `fetch`, no `fs`, no `window`, no npm
  runtime dependencies. You inject your own `FittingDataset`, so it runs in the browser,
  in Node, or in a worker, against whichever SDE snapshot you keep.
- **Node (`eve-fit-engine/node`)** — batteries included. Ships a version-pinned snapshot of
  the EVE Static Data Export plus a loader, so an EFT string in gives full stats out with
  nothing else to set up.

```ts
import { computeFromEft } from 'eve-fit-engine/node'

const { computed } = await computeFromEft(`
[Rifter, My Fit]
200mm AutoCannon II, Republic Fleet EMP S
200mm AutoCannon II, Republic Fleet EMP S
1MN Afterburner II
Gyrostabilizer II
`)

computed.derived.offense.totalDps
computed.derived.defense.ehpTotalAgainstProfile
computed.derived.navigation.maxVelocity
```

Skills default to all-V; pass a `skillProfile`, `damageProfile` or `targetProfile` to
override.

## Correctness

The engine is validated against [Pyfa](https://github.com/pyfa-org/Pyfa) two ways, because
a fitting engine that is *nearly* right is a fitting engine nobody can trust:

- **Fixture suite** — 662 hand-curated assertions against Pyfa, all-V skills, zero
  tolerance. This is the release gate.
- **Differential harness** — generates four fits for *every* published ship and compares
  every stat against a headless Pyfa oracle. **1662 of 1676 fits (99.2%) match exactly**;
  the residual is a documented set of Pyfa float and per-ship modelling quirks, listed in
  the repository rather than hidden.

## Licensing

The engine is **GPL-3.0-or-later**: it is a derivative work of Pyfa, whose calculation
semantics it mirrors, and it is distributed under the same terms. The complete
corresponding source is the linked repository.

The bundled SDE snapshot is included by mere aggregation and is **not** covered by the
GPL — it remains governed by the EVE Online Developer License Agreement. See `NOTICE` and
`data/SDE-LICENSE.md` in the repository.
