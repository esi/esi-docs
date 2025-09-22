---
title: Static Data
---

# Static Data

The Static Data Export (SDE) contains static game data that only changes with game updates.
The latest SDE can be found at: [developers.eveonline.com/static-data/](https://developers.eveonline.com/static-data/)

## Data formats

The SDE is available in two formats:

- [JSON Lines](https://jsonlines.org/)
- [YAML](https://yaml.org/)

### JSON Lines

JSON keys must be strings.
When the dataset contains integer keys, these are converted to a list format where each entry contains:

- `_key`: The actual key value.
- `_value`: The value (when the value is not an object).

### YAML

YAML supports integer keys, so it does not require the special encoding used in JSON Lines.
Note that reading large YAML files can be memory-intensive and slow.
When working with large datasets such as `mapMoons` and similar files, consider using the JSON Lines format.

## Schema Changes

Schema changes are documented at: [developers.eveonline.com/static-data/tranquility/schema-changelog.yaml](https://developers.eveonline.com/static-data/tranquility/schema-changelog.yaml)

## Automation

For automated access to the SDE:

- **Latest Build Number**: [developers.eveonline.com/static-data/tranquility/latest.jsonl](https://developers.eveonline.com/static-data/tranquility/latest.jsonl).
    - The latest build number is in the record with the key `sde`.
- **Data URLs**: `https://developers.eveonline.com/static-data/tranquility/eve-online-static-data-<build-number>-<variant>.zip`.
- **Changes**: `https://developers.eveonline.com/static-data/tranquility/changes/<build-number>.jsonl`.
    - This contains the list of changes.
      The record with key `_meta` contains `lastBuildNumber`, referring to the previous SDE.

Lastly, there are a few short-hand URLs to always fetch the latest version.
This will redirect to the URL with the latest build number.

- JSON Lines: [developers.eveonline.com/static-data/eve-online-static-data-latest-jsonl.zip](https://developers.eveonline.com/static-data/eve-online-static-data-latest-jsonl.zip)
- YAML: [developers.eveonline.com/static-data/eve-online-static-data-latest-yaml.zip](https://developers.eveonline.com/static-data/eve-online-static-data-latest-yaml.zip)

## HTTP Caching

All resources fully support ETag and Last-Modified headers.
Resources will only update when they actually change.
All non-static files are cached for 5 minutes.

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
