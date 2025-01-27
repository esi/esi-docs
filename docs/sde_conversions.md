<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

# SDE Conversions

Originally, the SDE was provided solely as an MS SQL server backup file. As the SDE is commonly used in environments where MS SQL is not available or would be overkill, a number of people maintain conversion routines and copies, to make it available in a more useful format.

As more formats were introduced, containing extra data, these routines were expanded to bring the data back into a single format.

As the various methods for conversion result in differing versions, with different layouts of data, conversions will be listed by the primary maintainer.

## [Steve Ronuken - Fuzzwork Enterprises](https://www.fuzzwork.co.uk/dump/)

Steve provides conversions of the SDE for download, in the following formats:

* SQL Server
* MySQL (both [full database](https://www.fuzzwork.co.uk/dump/mysql-latest.tar.bz2) and [single table](https://www.fuzzwork.co.uk/dump/latest/))
* [Postgres](https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2) (both public schema, and evetools schema)
* [SQLite](https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2)
* [CSV/XLS](https://www.fuzzwork.co.uk/dump/latest/) (depending on row counts)

.bz2 files can be unzipped with 7zip, on Windows.
Historical copies are kept available. When data is migrated into alternate formats, it's generally copied back into the old table format, but not always. The industry data, for example, is in a number of new industryActivity tables. While allowing for greater flexibility, this can break some older tools.

Conversion is performed with [https://github.com/fuzzysteve/yamlloader](https://github.com/fuzzysteve/yamlloader) which can target any database which SQLAlchemy can work with.

## [Squizz Caphinator - zKillboard](http://sde.zzeve.com/)

Tables from Steve's conversion converted into JSON files, with CORS headers.

* [List of tables](http://sde.zzeve.com/tables.json)
* [Source code](https://github.com/cvweiss/sde2json/)

## [EVE SDE Database Builder - by Zifrian](https://forums.eveonline.com/default.aspx?g=posts&t=500859)
EVE SDE Database Builder is a Windows application that lets users import the SDE yaml files into MS Access, MS SQL Server, Comma Separated Values, Semi-colon Separated Values, MySQL, PostgreSQL, and SQLite. Additionally, users can customize the import by language type and selecting specific SDE yaml files to import or ignore.

Main links for the application:
* [Screenshot of the program](http://i.imgur.com/iQIyUrw.png)
* [Binaries for installing the program](https://github.com/EVEIPH/EVE-SDE-Database-Builder/raw/master/Latest%20Files/EVE%20SDE%20Database%20Builder%20Install.zip)
* [SQL Schema used](https://github.com/EVEIPH/EVE-SDE-Database-Builder/blob/master/Latest%20Files/EVESDEDB_Schema.sql)
* [Github for the code](https://github.com/EVEIPH/EVE-SDE-Database-Builder)
