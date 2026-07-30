---
search:
  exclude: true

title: Fuzzwork Enterprises SDE Conversion
type: resource
description: SDE conversions, in Mysql/MariaDB, Postgres, SQLite, MSSql and CSV
maintainer:
  name: Steve Ronuken/Fuzzysteve
  github: https://github.com/fuzzysteve/
  repository: https://www.fuzzwork.co.uk/dump/
---

# Fuzzwork Enterprises SDE Conversion

Conversions of the Eve Static Data Extract, converted to mysql, postgres, sqlite or MSSQL, along with dumps of each table as a CSV file.

<div class="grid cards" markdown>

- [:octicons-browser-16: __Website__](https://www.fuzzwork.co.uk/dump/){ .esi-card-link }
- [:octicons-mark-github-16: __GitHub__](https://github.com/fuzzysteve/){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.gg/VzjYmKNUr){ .esi-card-link }

</div>

## Features

The EVE SDE is available as a zip file with JSONL or YAML files. this is great for transfer, but not so useful for lookups. These conversions allow you to treat the data as a relational database, and pull things out as you need them. 

Available as:

* SQLite DB
* MySQL/MariaDB
* Postgres in the public schema
* Postgres in an evesde schema
* MSSQL backup.
* CSV files
