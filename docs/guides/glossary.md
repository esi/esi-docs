# Glossary

This document is a list of common or unusual terms used in EVE third-party development and their meanings.

### APIs & Data sources

* [*ESI*](../services/esi/overview.md) — "EVE Swagger Interface"  
  The official RESTful API for EVE third-party development
* [*SDE*](../services/sde/index.md) — "Static Data Export"  
  Export of static game data (only changing with game updates)  
* *CREST* — "Carbon RESTful API"  
  Previous generation third-party development API (defunct since 2018)  
* *XML API*  
  Previous generation third-party development API (defunct since 2018)  
* *IGB* — "In-Game Browser"  
  In-game browser and related APIs (defunct since 2016)  
* *Static Data Dump*  
  Prior version of the *SDE*  

### Data Formats

* [*EFT*](./fitting.md#eft) — "EVE Fitting Tool"  
  Human-Readable format for ship fittings from the now-defunct third-party program of the same name, used in-game for fit copying and pasting 
* [*Ship DNA*](./fitting.md#dna)  
  Compact data format for ship fittings, used in-game for fit links
* [*XML Fitting*](./fitting.md#xml)  
  XML-based fitting format, used in-game for file-based fit export/import

### Data Types

* *Type*  
  Game object. Types describe most "things" in the game; cargo items, ships, objects in space  
  Found in the SDE in `fsd/types.yaml`, through ESI under `/universe/types/`  
* *Item*  
  An individual instance of a type; e.g., Type 648 ("Badger") describes all Badger ships, any individual assembled ship has a unique `itemID`.  
  An "object" as opposed to a "class" in programming terms  
* *Group*  
  Collection of related *Types*  
  Not to be confused with *MetaGroup* or *MarketGroup*  
  Found in the SDE in `fsd/groups.yaml`, through ESI under `/universe/groups/`  
* *Category*  
  Collection of related *Groups*  
  Usually differentiates the "kind" of object; E.g. "Ship" and "Module" are different Categories  
  Found in the SDE in `fsd/categories.yaml`, through ESI under `/universe/categories/`  
* *MetaGroup*  
  Tech-tier such as T1/T2/T3/Faction  
  Not to be confused with regular item *Group* or *MarketGroup*  
  Found in the SDE in `fsd/metaGroups.yaml`, not available through ESI  
* *MarketGroup*  
  A single tab (or tab group) in the market  
  Not to be confused with regular item *Group* or *MetaGroup*  
  Found in the SDE in `fsd/marketGroups.yaml`, through ESI under `/markets/groups/`  
* *Icon*  
  Icon images, such as inventory icons, UI icons, overview icons, etc.  
  Found in the SDE in `fsd/iconIDs.yaml`, not available through ESI  
* *Graphic*  
  Data about 3D models; Model geometry, textures, icons/renders of those models  
  Found in the SDE in `fsd/graphicIDs.yaml`, through ESI under `/universe/graphics/`  
* *Attribute*  
  (Additional) properties of a *Type*, such as HP, maximum velocity, and other item stats  
  Found in the SDE in `fsd/dogmaAttributes.yaml`, through ESI under `/dogma/attributes/`  
* *Effect*  
  Game logic element. Describes interactions between attributes  
  Some properties are also stored as effects rather than attributes (E.g. which slot a module uses)  
  Found in the SDE in `fsd/dogmaEffects.yaml`, through ESI under `/dogma/effects/`  

### Technical & other terms

* *BSD* — "Branched Static Data"  
  Old authoring format for game data, not all data has been ported over to the new *FSD* "File Static Data"  
  No meaningful difference to *FSD* for users  
* *FSD* — "File Static Data"  
  New authoring format for game data, not all data has been ported over  
  No meaningful difference to *BSD* for users  
* *Dogma*  
  Collective term for *Attributes*, *Effects* and the game logic around them  
* *Monolith*  
  The EVE Online servers (in particular, the database) for the game itself, as opposed to other services like *ESI*  
