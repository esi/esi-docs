# ID Ranges

A lot of entities in EVE have a sequential identifier.
These identifiers are grouped into ranges based on the type of entity they represent.
This document lists the ranges and the entities they represent.

The ranges are inclusive, meaning that the first and last ID in the range are valid IDs, however (except ID 0), the first ID is generally not used.

Keep in mind it is not possible to tell if an ID is a character, as characters created before 2010-11-03 share ID ranges with other entities (corporations and alliances).

| From              | To            | Description                                                          |
| ----------------- | ------------- | -------------------------------------------------------------------- |
| 0                 | 499,999       | [Various](#various) (often reused between different types)           |
| 500,000           | 599,999       | Factions                                                             |
| 1,000,000         | 1,999,999     | NPC corporations                                                     |
| 3,000,000         | 3,999,999     | NPC characters (agents and NPC corporation CEOs)                     |
| 9,000,000         | 9,999,999     | Universes                                                            |
| 10,000,000        | 19,999,999    | [Regions](#regions)                                                  |
| 20,000,000        | 29,999,999    | [Constellations](#constellations)                                    |
| 30,000,000        | 39,999,999    | [Solar systems](#solar-systems)                                      |
| 40,000,000        | 49,999,999    | Celestials (suns, planets, moons, asteroid belts)                    |
| 50,000,000        | 59,999,999    | Stargates                                                            |
| 60,000,000        | 69,999,999    | [Stations](#stations)                                                |
| 70,000,000        | 79,999,999    | Asteroids                                                            |
| 80,000,000        | 80,099,999    | Control Bunkers                                                      |
| 81,000,000        | 81,999,999    | WiS Promenades                                                       |
| 82,000,000        | 84,999,999    | Planetary Districts                                                  |
| 90,000,000        | 97,999,999    | EVE characters created between 2010-11-03 and 2016-05-30             |
| 98,000,000        | 98,999,999    | EVE corporations created after 2010-11-03                            |
| 99,000,000        | 99,999,999    | EVE alliances created after 2010-11-03                               |
| 100,000,000       | 2,099,999,999 | EVE characters, corporations and alliances created before 2010-11-03 |
| 2,100,000,000     | 2,111,999,999 | EVE / DUST characters created after 2016-05-30                       |
| 2,112,000,000     | 2,129,999,999 | EVE characters created after 2016-05-30                              |
| 1,000,000,000,000 | -             | Spawned items                                                        |

## Various

### Factional Warfare Complexes

| ID  | Description    |
| --- | -------------- |
| 33  | Novice Complex |
| 34  | Small Complex  |
| 35  | Medium Complex |
| 36  | Large Complex  |

### Signature Types

| ID   | Description |
| ---- | ----------- |
| 208  | Data Site   |
| 209  | Gas Site    |
| 210  | Relic Site  |
| 211  | Ore Site    |
| 1136 | Combat Site |
| 1908 | Wormhole    |

## Regions

| From       | To         | Description                    |
| ---------- | ---------- | ------------------------------ |
| 10,000,000 | 10,999,999 | New Eden (known space) regions |
| 11,000,000 | 11,999,999 | Wormhole regions               |
| 12,000,000 | 12,999,999 | Abyssal regions                |
| 14,000,000 | 14,999,999 | Void regions                   |
| 19,000,000 | 19,999,999 | Global Plex market regions  |

## Constellations

| From       | To         | Description                           |
| ---------- | ---------- | ------------------------------------- |
| 20,000,000 | 20,999,999 | New Eden (known space) constellations |
| 21,000,000 | 21,999,999 | Wormhole constellations               |
| 22,000,000 | 22,999,999 | Abyssal constellations                |
| 24,000,000 | 24,999,999 | Void constellations                   |

## Solar systems

| From       | To         | Description                          |
| ---------- | ---------- | ------------------------------------ |
| 30,000,000 | 30,999,999 | New Eden (known space) solar systems |
| 31,000,000 | 31,999,999 | Wormhole solar systems               |
| 32,000,000 | 32,999,999 | Abyssal systems                      |
| 34,000,000 | 34,999,999 | Void systems                         |

## Stations

| From       | To         | Description                            |
| ---------- | ---------- | -------------------------------------- |
| 60,000,000 | 60,999,999 | NPC stations                           |
| 61,000,000 | 63,999,999 | Outposts                               |
| 66,000,000 | 67,999,999 | Station folders of corporation offices |
| 68,000,000 | 68,999,999 | Station folders for NPC stations       |
| 69,000,000 | 69,999,999 | Station folders for outposts           |
