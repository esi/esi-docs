# EVE Image Server (EIS)

The EVE Image Server provides a way to retrieve/use images from EVE Online in your applications.

## Images

The Image server can be accessed at the following URL: `https://images.evetech.net/{category}/{id}/{variation}` with the following parameters:

- `{category}`: The category of the image you want to retrieve. This can be one of the following:
    - `alliances`
    - `characters`
    - `corporations`
    - `types`
- `{id}`: The ID of the `{category}` you want to retrieve the image for.
- `{variation}`: The variation of the image you want to retrieve.
  If you don't specify a variation, the server will return a JSON array of available variations for the given `{category}` and `{id}`.
  In general, alliances and corporations will have a `logo` variation, characters will have a `portrait` variation.
  Types will have variations depending on what kind of type it is.

### Query Parameters

There are two supported query parameters: `size` and `tenant`.

Valid values for the `size` parameter include powers-of-two ranging between 32 and 1024.
If this parameter is not provided, the server will return the image in its original size.

The `tenant` parameter defines the server for which to request images. This defaults to `tranquility`, but also accepts `singularity`.

### Notes

- NPC faction logos are available in the `corporations` category using their faction ID.
- The ID 1 can be used with alliances, corporations and characters to retrieve the default logo/portrait.
- Images are returned as PNGs, with the exception of character portraiuts, which are returned as JPEGs.
- You are welcome to point your clients and applications directly at the image service and use it as a CDN. You do not need to cache images locally.

## Examples

|                 Category  | Variation | Example                                                                                |
| ------------------------: | --------- | -------------------------------------------------------------------------------------- |
|                  Alliance | Logo      | ![Alliance Logo](https://images.evetech.net/alliances/99011477/logo?size=64)           |
|               Corporation | Logo      | ![Corporation Logo](https://images.evetech.net/corporations/1686954550/logo?size=64)   |
| Corporation (NPC Faction) | Logo      | ![Corporation Logo](https://images.evetech.net/corporations/500001/logo?size=64)       |
|                 Character | Portrait  | ![Character Portrait](https://images.evetech.net/characters/91072482/portrait?size=64) |
|                      Type | Render    | ![Type Render](https://images.evetech.net/types/587/render?size=64)                    |
|                      Type | Icon      | ![Type Render](https://images.evetech.net/types/587/icon?size=64)                      |
|                      Type | BPO       | ![Type Render](https://images.evetech.net/types/11568/bp?size=64)                      |
|                      Type | BPC       | ![Type Render](https://images.evetech.net/types/11568/bpc?size=64)                     |
|                      Type | Relic     | ![Type Render](https://images.evetech.net/types/30752/relic?size=64)                   |
