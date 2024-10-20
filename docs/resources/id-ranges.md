# ID Ranges

A lot of entities in EVE have a sequential identifier. These identifiers are grouped into ranges based on the type of entity they represent. This document lists the ranges and the entities they represent.

The ranges are inclusive, meaning that the first and last ID in the range are valid IDs, however (with the exception of ID 0), the first ID is generally not used to avoid overlap with other ranges.


| From          | To            | Description                                                            |
| --------------|---------------|----------------------------------------------------------------------- |
| 0             | 10,000        | System items (including junkyards and other special purpose items)     |
| 500,000       | 1,000,000     | Factions                                                               |
| 1,000,000     | 2,000,000     | NPC corporations                                                       |
| 3,000,000     | 4,000,000     | NPC characters (agents and NPC corporation CEO's)                      |
| 9,000,000     | 10,000,000    | Universes                                                              |
| 10,000,000    | 11,000,000    | New Eden regions                                                       |
| 11,000,000    | 12,000,000    | Wormhole regions                                                       |
| 12,000,000    | 13,000,000    | Abyssal regions                                                        |
| 20,000,000    | 21,000,000    | New Eden constellations                                                |
| 21,000,000    | 22,000,000    | Wormhole constellations                                                |
| 22,000,000    | 23,000,000    | Abyssal constellations                                                 |
| 30,000,000    | 31,000,000    | New Eden solar systems                                                 |
| 31,000,000    | 32,000,000    | Wormhole solar systems                                                 |
| 32,000,000    | 33,000,000    | Abyssal systems                                                        |
| 40,000,000    | 50,000,000    | Celestials (suns, planets, moons, asteroid belts)                      |
| 50,000,000    | 60,000,000    | Stargates                                                              |
| 60,000,000    | 61,000,000    | Stations created by CCP                                                |
| 61,000,000    | 64,000,000    | Stations created from outposts                                         |
| 68,000,000    | 69,000,000    | Station folders for stations created by CCP                            |
| 69,000,000    | 70,000,000    | Station folders for stations created from outposts                     |
| 70,000,000    | 80,000,000    | Asteroids                                                              |
| 80,000,000    | 80,100,000    | Control Bunkers                                                        |
| 81,000,000    | 82,000,000    | WiS Promenades                                                         |
| 82,000,000    | 85,000,000    | Planetary Districts                                                    |
| 90,000,000    | 98,000,000    | EVE characters created after 2010-11-03                                |
| 98,000,000    | 99,000,000    | EVE corporations created after 2010-11-03                              |
| 99,000,000    | 100,000,000   | EVE alliances created after 2010-11-03                                 |
| 100,000,000   | 2,100,000,000 | EVE characters, corporations and alliances created before 2010-11-03   |
| 2,100,000,000 | 2,147,483,647 | DUST characters, EVE characters created after 2016-05-30               |