<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

## Resolving Upwell Structure IDs

A common scenario is to resolve a structure ID into a name. Use the authenticated `/universe/structures/{structure_id}/` endpoint for that. It requires a token that grants the `esi-universe.read_structures.v1` scope on a character that has docking access to the structure. 

The endpoint returns the name of the structure, as well as some additional information such as its system id, type id and the owner corporation id.

## Discovering Upwell Structures

There is currently no unified way to discover accessible Upwell structures through ESI. The following methods can be used to discover Upwell structure IDs.

### Public Structures

The public `/universe/structures/` endpoint will return a flat list of IDs containing all fully public structures. *Fully public* in this context means a completely open Access Control List. If the ACL prevents even one character from docking the structure won't show up in this list.

This method has the advantage of not requiring any authentication but is limited in that it only resolves completely public structures. Additionally, most endpoints that consume structure IDs require authentication anyways, so you likely won't be possible to avoid supplying a token anyways.

### Corporation Structures

The authenticated `/corporations/{corporation_id}/structures/` endpoint returns all structures owned by a particular corporation. It requires a token that grants the `esi-corporations.read_structures.v1` scope on a character with the Director role in the corporation.

This endpoint provides a lot of information about the structure, including what services are installed and active, when the fuel expires, what state it currently is in etc. Be aware that it currently *does not* provide the name of the structure.

### Other endpoints

Some other endpoints may also include structure ids in their results. Structure IDs can usually be distinguished because they are in the int64 range while currently most other IDs are in the int32 range. The following endpoints will often return structure IDs:

- All contract endpoints may have location_ids that are structures
- Character and Corporation asset location_ids
- Character Location
- Clone locations
- Fleet member station_id may be structure ids
- Industry jobs may be located in structure ids
- Character and Corporation market orders may have location_ids that are structures.
