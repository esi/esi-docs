# Using Static Data

This page provides additional information and specific guides for using the Static Data Export.

For information on how to download or automate access to the Static Data Export, see the [Services and Resources page.](../services/static-data/index.md)

## Celestial names

In the SDE there is generally no mention of the name of stars, planets, moons, asteroid belts, and NPC stations.
This is because they can be deduced from the solar system name, and a few fields related to the celestial object.

There are a few exceptions; in those cases the celestial has a `name` field with their name.
In all other cases, follow the below table.

| Celestial                                      | Content                                           |
|------------------------------------------------|---------------------------------------------------|
| Stars                                          | `<solarSystemName>`                               |
| Planets                                        | `<orbitName> <celestialIndex>`                    |
| Moons                                          | `<orbitName> - Moon <orbitIndex>`                 |
| Asteroid Belts                                 | `<orbitName> - Asteroid Belt <orbitIndex>`        |
| Stations (where `useOperationName` is true)    | `<orbitName> - <corporationName> <operationName>` |
| Stations (where `useOperationName` isn't true) | `<orbitName> - <corporationName>`                 |
| Stargates                                      | `Stargate (<solarSystemName>)`                    |

Note:

- For stars, use `solarSystemID` to look up the `solarSystemName` via `mapSolarSystems` (as `name`).
- The `orbitName` is the name of the `orbitID` celestial, constructed via the table above.
- The `celestialIndex` should be represented in Roman numerals.
- For stations, use `ownerID` to look up the `corporationName` via `npcCorporations` (as `name`).
- For stations, use `operationID` to look up the `operationName` via `stationOperations`.
- For stargates, use `destination.solarSystemID` to look up the `solarSystemName` via `mapSolarSystems` (as `name`).

Localization:

The following strings are used for the other languages supported by EVE Online.
Formatting uses the same rules above.

| en-us (English) | Moon | Asteroid Belt          | Stargate          |
|-----------------|------|------------------------|-------------------|
| zh (Chinese)    | 卫星   | 小行星带                   | 星门                |
| fr (French)     | Lune | Ceinture d'astéroïdes  | Portail stellaire |
| de (German)     | Moon | Asteroid Belt          | Stargate          |
| ja (Japanese)   | 衛星   | アステロイドベルト              | スターゲート            |
| ko (Korean)     | 위성   | 소행성 벨트                 | 스타게이트             |
| ru (Russian)    | Moon | Asteroid Belt          | Stargate          |
| es (Spanish)    | Luna | Cinturón de asteroides | Portal estelar    |

## Security Office

The SDE lists stations having a Security Office; however, only the ones in [Lowsec](system-security.md)-located CONCORD / DED stations are available to players.

## TypeLists

Some sets of types don't map cleanly onto 'Groups' or 'Categories'. TypeLists describe arbitrary sets of types and are used for a variety of purposes, such as the different groupings of ore, the groups of ships that are allowed to enter certain acceleration gates, or which objects generate a killmail when destroyed.

TypeLists are available in the SDE's `typelists` file.

A TypeList consists of a set of included Categories, Groups, and Types, and a set of excluded Categories, Groups, and Types. To get the full list of all types in a TypeList, do the following (in this order):

1. Add all items with a category in `includedCategoryIDs` to the list.
2. Remove all items with a category in `excludedCategoriesIDs` from the list. 
3. Add all items with a group in `includedGroupIDs` to the list.
4. Remove all items with a group in `excludedGroupIDs` from the list.
5. Add all items in `includedTypeIDs` to the list.
6. Remove all items in `excludedTypeIDs` from the list.

!!! example
    ```
    {
        includedCategoryIDs: [6],       // All ships
        excludedGroupIDs:    [420],     // But not T1 destroyers
        includedTypeIDs:     [16240],   // But including the Catalyst
    }
    ```
    `includedTypeIDs` takes precedence over `excludedGroupIDs`, so this list does include the Catalyst (typeID 16240), but excludes the other T1 destroyers, and including all non-destroyer ships.

!!! tip
    Some typelists have a `displayName` and/or `displayDescription`, succinctly explaining list.

--8<-- "snippets/examples/staticdata-typelist.md"

## Remote Skill Purchasing

Skills are commonly unlocked by buying skillbook items on the in-game market. Certain skills can be bought directly from the character sheet's Skill Catalogue, also known as "Skills On Demand" or "Remote Skill Injection". Some skills are unavailable as skillbook item and must be purchased directly in the character sheet.

The skills that are available for direct purchase are provided by [TypeList](#typelists) #93 "Skills available for purchase", at 130% of the Skill's `basePrice` (from the `types` file).

## Mercenary Tactical Operations & Dungeons

Mercenary Tactical Operations and some other deadspace sites permit only certain ships to enter, locked behind an Acceleration Gate. 
The SDE provides basic information about such sites in the `dungeons` file. Including Name, Archetype (Dungeon group), and the Allowed Ships. No information is provided about the NPCs or other hazards encountered, nor potential rewards. Such information may be gathered in-game or acquired from another player who has already done so.

Additional information specific to Mercenary Tactical Operations is available in the `mercenaryTacticalOperations` file. Such as the impacts on Anarchy and Development scores and infomorph production.

This data is generally used in conjunction with ESI endpoints like [`/characters/{character_id}/mercenary-tactical-operations/{operation_id}`](/api-explorer#/operations/GetCharactersMercenaryTacticalOperationsDetail).

!!! example "Example: *FC, can I bring my drake?*"
    For a given Mercenary Tactical Operation ("Rogue Drone Emergence", #12367), and ship ("Drake", #24698):
    
    The Operation name & impacts can be retrieved from `mercenaryTacticalOperations` with the dungeonID as key:
    ```json
    {"_key": 12367, "anarchyImpact": -20, "description": { /* omitted */ }, "developmentImpact": 10, "dungeonID": 12367, "infomorphBonus": 350, "name": { /* omitted */ }}
    ```
    The Operation's dungeon info can be retrieved from `dungeons` with the dungeonID as key:

    ```json
    {"_key": 12367, "allowedShipsList": [793], "archetypeID": 80, "factionID": 500021, "name": { /* omitted */ }}
    ```
    
    The ships allowed access to the site are specified in the `allowedShipsList` typeList (Note: A dungeon can specify multiple allow-lists, a ship is allowed if it matches any)  
    For this dungeon, the allow-list is TypeList #793, which can be retrieved from `typeLists` static data:

    ```json
    {"_key": 793, "includedGroupIDs": [26, 25, 420, 324, 830, 893, 1283, 831, 1527, 1534, 541, 1305, 834], "name": "Mercenary Den - Ship Restriction list"}
    ```
    
    The ship can then be matched against this [(TypeList)](#typelists).  
    The Drake, having Group "Combat Battlecruiser" #419, is not included on this list and is not allowed to enter the Mercenary Tactical Operation.

## Wormhole Classes & Effects

Information about the "wormhole class" and "wormhole effects" of solarsystems in wormhole space is available in the SDE.
No information is provided to third party developers about the "static wormholes" of a system. Such information may be gathered in-game or acquired from another player who has already done so.

### Wormhole Classes

Solarsystems, Constellations, and Regions in the game have an optional associated `wormholeClassID`.  
This value is provided in the respective map data file. (`mapSolarSystems`,`mapConstellations`, `mapRegions`)

A system with no wormholeClassID value inherits it from the Constellation, or from the Region if the Constellation also has no wormholeClassID set. If neither system, nor constellation, nor region has a wormholeClassID set, the system has no assigned wormholeClassID.

WormholeClass IDs 1 through 6 correspond with the common wormhole classes one through six. Rarer wormhole systems and non-wormhole systems have other IDs. (See table)

!!! warning
    These wormholeClassIDs are not suitable for identifying other kinds of space like Abyssal Space, Highsec, or Nullsec; Not all systems have a wormholeClassID assigned. 
    
    For such differentiation [ID ranges](./id-ranges.md) and [System Security](./system-security.md) must be used instead.

| WormholeClassID    | System kind                                                                     |
|--------------------|---------------------------------------------------------------------------------|
| 1                  | Class 1 Wormhole Space System                                                   |
| 2                  | Class 2 Wormhole Space System                                                   |
| 3                  | Class 3 Wormhole Space System                                                   |
| 4                  | Class 4 Wormhole Space System                                                   |
| 5                  | Class 5 Wormhole Space System                                                   |
| 6                  | Class 6 Wormhole Space System                                                   |
| 7                  | Highsec New Eden / "Known Space" System                                         |
| 8                  | Lowsec New Eden / "Known Space" System                                          |
| 9                  | Nullsec New Eden / "Known Space" System                                         |
| 10 & 11            | (Unused, QA only) Jove Space constellations "0VFS-G" and "B-HLOG"               |
| 12                 | Thera                                                                           |
| 13                 | Special "Frigate only" Shattered Wormhole Systems                               |
| 14, 15, 16, 17, 18 | "Drifter" Wormhole Systems (Sentinel, Barbican, Vidette, Conflux, Redoubt)      |
| 19, 20, 21, 22, 23 | Abyssal Space (Unused; No wormholes)                                            |
| 24                 | Unused                                                                          |
| 25                 | Pochven                                                                         |
| -1                 | (Special) Not assigned to any system, used by C729 wormholes leading to Pochven |

### Wormhole Effects

Certain solarsystems in wormhole space have a 2nd "star" and effect on ships, boosting certain attributes and reducing others.

Information about this is provided by `mapSecondarySuns` file, which details these second "star"/sun objects & their effects.
Each entry has a celestialID, unique for the SecondarySun, the `solarSystemID` of the system having this effect, a `typeID` of the SecondarySun which identifies what kind of effect (see table below), an `effectBeaconTypeID`, and finally a `position`.

The `typeID` describes what kind of effect the system has, and is shared between all wormhole classes.  
The `effectBeaconID` links to an effect beacon item, which is unique per-class per-effect and provides the Dogma for the effect applied to ships.  
The `position` field has no meaning; Unlike the normal Stars, the "SecondarySun" cannot be warped to or visited.

| TypeID | Name                 |
|--------|----------------------|
| 30574  | Magnetar             |
| 30575  | Black Hole           |
| 30576  | Red Giant            |
| 30577  | Pulsar               |
| 30669  | Wolf-Rayet star      |
| 30670  | Cataclysmic Variable |


!!! example

    Starting with solarsystem "J105934" (SolarSystemID `31002487`):

    1. Look up the mapSolarSystems information -> No wormholeClassID specified for this system, constellationID is `21000298`
    2. Look up the mapConstellations information the system's constellation -> No wormholeClassID specified for constellation `21000298` ("F-C00298"), regionID is `11000030`
    3. Look up the mapRegions information for the system's region -> Region `11000030` ("F-R00030") has wormholeClassID `6`
    4. Look up the mapSecondarySuns information, searching for the entry with solarSystemID `31002487` -> This system contains Secondary Sun #`40486155`, whose typeID is `30574` "Magnetar"

    Solarsystem "J105934" (SolarSystemID `31002487`) is a Class 6 Magnetar wormhole system.