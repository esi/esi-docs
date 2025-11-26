# Glossary

This document is a list of common or unusual terms used in EVE third-party development and their meanings.

### APIs & Data sources

* [*ESI*](../services/esi/overview.md) — "EVE Swagger Interface"<br>
  The official RESTful API for EVE third-party development.
* [*SDE*](../services/static-data/index.md) — "Static Data Export"<br>
  Export of static game data (only changing with game updates).
* *CREST* — "Carbon RESTful API"<br>
  Previous generation third-party development API (defunct since 2018).
* *XML API*<br>
  Previous generation third-party development API (defunct since 2018).
* *IGB* — "In-Game Browser"<br>
  In-game browser and related APIs (defunct since 2016).
* *Static Data Dump*<br>
  Prior version of the *SDE*.

### Data Formats

* [*EFT*](./fitting.md#eft) — "EVE Fitting Tool"<br>
  Human-Readable format for ship fittings from the now-defunct third-party program of the same name, used in-game for fit copying and pasting.
* [*Ship DNA*](./fitting.md#dna)<br>
  Compact data format for ship fittings, used in-game for fit links.
* [*XML Fitting*](./fitting.md#xml)<br>
  XML-based fitting format, used in-game for file-based fit export/import.

### Data Types

* *Type*<br>
  Game object. Types describe most "things" in the game; cargo items, ships, objects in space.<br>
  Found in the SDE in `types.yaml`, through ESI under `/universe/types/`.
* *Item*<br>
  An individual instance of a type; e.g., Type 648 ("Badger") describes all Badger ships, any individual assembled ship has a unique `itemID`.<br>
  An "object" as opposed to a "class" in programming terms.
* *Group*<br>
  Collection of related *Types*.<br>
  Not to be confused with *MetaGroup* or *MarketGroup*.<br>
  Found in the SDE in `groups.yaml`, through ESI under `/universe/groups/`.
* *Category*<br>
  Collection of related *Groups*.<br>
  Usually differentiates the "kind" of object; E.g. "Ship" and "Module" are different Categories.<br>
  Found in the SDE in `categories.yaml`, through ESI under `/universe/categories/`.
* *MetaGroup*<br>
  Tech-tier such as T1/T2/T3/Faction.<br>
  Not to be confused with regular item *Group* or *MarketGroup*.<br>
  Found in the SDE in `metaGroups.yaml`, not available through ESI.
* *MarketGroup*<br>
  A single tab (or tab group) in the market.<br>
  Not to be confused with regular item *Group* or *MetaGroup*.<br>
  Found in the SDE in `marketGroups.yaml`, through ESI under `/markets/groups/`.
* *Icon*<br>
  Icon images, such as inventory icons, UI icons, overview icons, etc.<br>
  Found in the SDE in `icons.yaml`, not available through ESI.
* *Graphic*<br>
  Data about 3D models; Model geometry, textures, icons/renders of those models.<br>
  Found in the SDE in `graphics.yaml`, through ESI under `/universe/graphics/`.
* *Attribute*<br>
  (Additional) properties of a *Type*, such as HP, maximum velocity, and other item stats.<br>
  Found in the SDE in `dogmaAttributes.yaml`, through ESI under `/dogma/attributes/`.
* *Effect*<br>
  Game logic element. Describes interactions between attributes.<br>
  Some properties are also stored as effects rather than attributes (E.g. which slot a module uses).<br>
  Found in the SDE in `dogmaEffects.yaml`, through ESI under `/dogma/effects/`.

### Technical & other terms

* *BSD* — "Branched Static Data"<br>
  Old authoring format for game data, not all data has been ported over to the new *FSD* "File Static Data".<br>
  No meaningful difference to *FSD* for users.<br>
* *FSD* — "File Static Data"<br>
  New authoring format for game data, not all data has been ported over.<br>
  No meaningful difference to *BSD* for users.
* *Dogma*<br>
  Collective term for *Attributes*, *Effects* and the game logic around them.
* *Monolith*<br>
  The EVE Online servers (in particular, the database) for the game itself, as opposed to other services like *ESI*.
