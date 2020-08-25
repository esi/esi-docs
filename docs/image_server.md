# Introduction
You can use this service to obtain images related to entities in New Eden. At this time, it is possible to get alliance logos, corp logos, character portraits, faction logos, ship renders and inventory type icons in various resolutions.

Corporation logos, alliance logos, inventory type icons and ship renders are returned as transparency-enabled 32 bit PNGs. Character portraits are returned as JPEGs.

If a given image is not found in the database, the service responds with a 302 Moved HTTP response and redirects the HTTP client to a generic image. If you request an image in an invalid size, you get a plain 404.

You are welcome to point your clients and applications directly at the image server and use it as a CDN. You do not need to cache the images and serve them yourself.

The base URL for the image server is https://images.evetech.net/

# Image Routes
## Alliance Images
* URL Pattern: `/Alliance/{allianceID}_{width}.png`
* Available Sizes: 32, 64, 128
* Samples:
    * [Band of Brothers](https://images.evetech.net/Alliance/632866070_128.png)
    * [GoonSwarm](https://images.evetech.net/Alliance/824518128_32.png)

## Corporation Images
* URL Pattern: `/Corporation/{corpID}_{width}.png`
* Available Sizes: 32, 64, 128, 256
* Samples:
    * [EVE University](https://images.evetech.net/Corporation/917701062_128.png)
    * [Love Squad](https://images.evetech.net/Corporation/98076155_256.png)

## Character Images
* URL Pattern: `/Character/{characterID}_{width}.jpg`
* Available Sizes: 32, 64, 128, 256, 512, 1024
* Note: the 1024 size images may not be available for all characters
* Samples:
    * [Large Collidable Object](https://images.evetech.net/Character/91072482_1024.jpg)
    * [Ice Driller](https://images.evetech.net/Character/1611454010_512.jpg)


## Faction Images
* URL Pattern: `/Alliance/{factionID}_{width}.png`
* Available Sizes: 32, 64, 128
* Samples:
    * [Gallente Federation](https://images.evetech.net/Alliance/500004_128.png)
    * [Amarr Empire](https://images.evetech.net/Alliance/500003_64.png)

## Inventory Types
* URL Pattern: `/Type/{typeID}_{width}.png`
* Available Sizes: 32, 64
* Samples:
    * [Domination Stasis Webifier](https://images.evetech.net/Type/14264_32.png)
    * [Exotic Dancers](https://images.evetech.net/Type/17765_64.png)

## Ship and Drone Renders
* URL Pattern: `/Render/{typeID}_{width}.png`
* Available Sizes: 32, 64, 128, 256, 512
* Samples:
    * [Machariel](https://images.evetech.net/Render/17738_512.png)
    * [Firbolg](https://images.evetech.net/Render/23059_128.png)


# Legacy Portraits
Legacy portraits are from before the change to the existing character creator that occurred on November 30th, 2010 with the release of the Incursion expansion. These renders let you see how characters that existed back then looked in the previous character creator.

* [Old Character Portraits](http://cdn1.eveonline.com/data/OldCharPortraits_256.zip)
