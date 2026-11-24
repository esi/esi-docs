---
title: Static Data
---

# Static Data

The Static Data Export (SDE) contains static game data, such as types, map data, and blueprints.
It is served by the SDE API at [sde.evetech.net](https://sde.evetech.net/).

You request a single record, a whole table, or everything at once, using plain HTTP requests.
The SDE API does not go through Tranquility, so it is not affected by the daily downtime.

## Exploring the API

Every response links to the next level, so you can browse down from the root:

- [sde.evetech.net](https://sde.evetech.net/) lists the tenants.
- [sde.evetech.net/tranquility/](https://sde.evetech.net/tranquility/) lists the releases, newest first.
- [sde.evetech.net/tranquility/latest/](https://sde.evetech.net/tranquility/latest/) shows the current release: its build number, its release date, and every table with its links.

## Formats

For each table, the following URLs are available (relative to the release URL):

| URL                    | Content                                                    |
|------------------------|------------------------------------------------------------|
| `<table>/<key>.json`   | A single record.                                           |
| `<table>.jsonl`        | The whole table in [JSON Lines](https://jsonlines.org/), one record per line. |
| `<table>.schema.json`  | The [JSON Schema](https://json-schema.org/) of a single record. |
| `<table>.fb`           | The whole table in [FlatBuffers](https://flatbuffers.dev/). |
| `<table>.fbs`          | The FlatBuffers schema.                                    |

For example, the Rifter is at [sde.evetech.net/tranquility/latest/types/587.json](https://sde.evetech.net/tranquility/latest/types/587.json).

FlatBuffers is a binary format that is very fast to read, especially when you only need a few fields from each record.

!!! note
    Files are always sent gzip-compressed.
    Most HTTP libraries handle this for you; with `curl`, add `--compressed`.

### Records

- Each record starts with its key, which has a proper name, like `typeID`.
  The JSON Schema tells you which field is the key.
- Numbers are plain JSON numbers: a mass of `1.0` is written as `1`.
  Very large values, like `massDust` on moons, are written as floats, so JavaScript and other languages can read them safely.
- Required fields are always present, even when empty.
  Optional fields are left out when they have no value.

## Downloading everything

To download every table in JSON Lines:

```bash
curl -sL --compressed https://sde.evetech.net/tranquility/latest/ \
  | jq -r '.tables[].jsonl.url' \
  | xargs -n1 -P8 curl -sSLO --compressed
```

The URLs returned by `latest/` point to that exact release, so all files belong together, even if a new release lands during the download.

## Releases

A new release is published whenever the data changes.
After a Tranquility deployment, it shows up in about 10 minutes.
Releases also happen outside of deployments, for example when new military campaign objectives start.

This means build numbers are not unique: several releases can share the same build number.
Use the `release` field to tell them apart.

- `/tranquility/latest/` always redirects to the current release.
- Every release has its own URL, like `/tranquility/20261116T124006Z/`.
  Use it when a batch of requests must all come from the same release.

!!! warning
    Only the current and the previous release are kept.
    Older release URLs stop working once their releases are no longer retained.

## Staying up to date

You do not have to download everything every time:

- Each table has a `version` field that only changes when the data in that table changes.
- All resources support the `ETag` header.
  Send it back in the `If-None-Match` header; if nothing changed, you get a `304 Not Modified`.

Every release also comes with two extra tables:

- `_changes` lists what changed since the previous release.
- `_schemaChangelog` lists the changes to the schemas.
