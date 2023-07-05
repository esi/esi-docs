# Image Server

The image service for EVE Online, formerly known as the image server, provides images of EVE Online entities.

The service is available at: [https://images.evetech.net/](https://images.evetech.net/)

## Images

Image URLs follow the format of `https://images.evetech.net/{category}/{id}/{variation}`, where category is one of `alliances`, `corporations`, `characters`, or `types`.

In order to request an image, a variation must be included. Alliances and corporations will have a `logo`, characters will have a `portrait`, while types can have several different variations. A list of available variations can be requested at `https://images.evetech.net/{category}/{id}`, and is returned as a JSON array of strings.

## Query Parameters

Two query parameters are supported: `size` and `tenant`.

Valid values for the `size` parameter include 32, 64, 128, 256, 512, and 1024. If it is not provided, the image will be returned in its native resolution.

The `tenant` parameter defines the server for which to request images. Defaults to `tranquility`, also supports `singularity`.

## Additional Notes

NPC faction logos are available by using the faction ID with the corporations category.

The ID 1 can be used with the alliances, corporations, and characters categories to return the default logo/portrait.

Images are returned as PNGs. An exception to this are character portraits, which are returned as JPEGs.

You are welcome to point your clients and applications directly at the image service and use it as a CDN. You do not need to cache the images and serve them yourself.

## Examples

- Alliances: [https://images.evetech.net/alliances/434243723](https://images.evetech.net/alliances/434243723)
  - [https://images.evetech.net/alliances/434243723/logo](https://images.evetech.net/alliances/434243723/logo)
- Corporations: [https://images.evetech.net/corporations/109299958](https://images.evetech.net/corporations/109299958)
  - [https://images.evetech.net/corporations/109299958/logo](https://images.evetech.net/corporations/109299958/logo)
- NPC Factions: [https://images.evetech.net/corporations/500001](https://images.evetech.net/corporations/500001)
  - [https://images.evetech.net/corporations/500001/logo](https://images.evetech.net/corporations/500001/logo) 
- Characters: [https://images.evetech.net/characters/1338057886](https://images.evetech.net/characters/1338057886)
  - [https://images.evetech.net/characters/1338057886/portrait](https://images.evetech.net/characters/1338057886/portrait)
- Rifter (type): [https://images.evetech.net/types/587](https://images.evetech.net/types/587)
  - [https://images.evetech.net/types/587/icon](https://images.evetech.net/types/587/icon)
  - [https://images.evetech.net/types/587/render](https://images.evetech.net/types/587/render)
- 250mm Railgun II (type): [https://images.evetech.net/types/3082](https://images.evetech.net/types/3082)
  - [https://images.evetech.net/types/3082/icon](https://images.evetech.net/types/3082/icon)
- Avatar Bleuprint (type): [https://images.evetech.net/types/11568](https://images.evetech.net/types/11568)
  - [https://images.evetech.net/types/11568/bp](https://images.evetech.net/types/11568/bp)
  - [https://images.evetech.net/types/11568/bpc](https://images.evetech.net/types/11568/bpc)
- Intact Hull Section (type): [https://images.evetech.net/types/30752](https://images.evetech.net/types/30752)
  - [https://images.evetech.net/types/30752/relic](https://images.evetech.net/types/30752/relic)

# Legacy Portraits
Legacy portraits are from before the change to the existing character creator that occurred on November 30th, 2010 with the release of the Incursion expansion. These renders let you see how characters that existed back then looked in the previous character creator.

* [Old Character Portraits](http://cdn1.eveonline.com/data/OldCharPortraits_256.zip)
