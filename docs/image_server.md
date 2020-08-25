# Introduction
You can use this service to obtain images related to entities in New Eden. At this time, it is possible to get alliance logos, corp logos, character portraits, faction logos, ship renders and inventory type icons in various resolutions.

Corporation logos, alliance logos, inventory type icons and ship renders are returned as transparency-enabled 32 bit PNGs. Character portraits are returned as JPEGs.

If a given image is not found in the database, the service responds with a 302 Moved HTTP response and redirects the HTTP client to a generic image. If you request an image in an invalid size, you get a plain 404.

You are welcome to point your clients and applications directly at the image server and use it as a CDN. You do not need to cache the images and serve them yourself.

The base URL for the image server is https://images.evetech.net/

# Image Routes
## Alliance Images
* URL Pattern: `/alliances/{alianceID}/logo?tenant={tenant}&size={size}`
* Available Sizes: 32, 64, 128, 256, 512 and 1024
* Samples:
    * [Band of Brothers](https://images.evetech.net/alliances/632866070/logo?tenant=tranquility&size=128)
    * [GoonSwarm](https://images.evetech.net/alliances/824518128/logo?tenant=tranquility&size=128)

## Corporation Images
* URL Pattern: `/corporations/{corpID}/logo?tenant={tenant}&size={size}`
* Available Sizes: 32, 64, 128, 256, 512 and 1024
* Samples:
    * [EVE University](https://images.evetech.net/corporations/917701062/logo?tenant=tranquility&size=128)
    * [Love Squad](https://images.evetech.net/corporations/98076155/logo?tenant=tranquility&size=128)

## Character Images
* URL Pattern: `/characters/{characterID}/portrait?tenant={tenant}&size={size}`
* Available Sizes: 32, 64, 128, 256, 512 and 1024
* Note: the 1024 size images may not be available for all characters
* Samples:
    * [Large Collidable Object](https://images.evetech.net/characters/91072482/portrait?tenant=tranquility&size=1024)
    * [Ice Driller](https://images.evetech.net/characters/1611454010/portrait?tenant=tranquility&size=1024)


## Faction Images
* URL Pattern: `/alliances/{alianceID}/logo?tenant={tenant}&size={size}`
* Available Sizes: 32, 64, 128, 256, 512 and 1024
* Samples:
    * [Gallente Federation](https://images.evetech.net/alliances/500004/logo?tenant=tranquility&size=128)
    * [Amarr Empire](https://images.evetech.net/alliances/5000063/logo?tenant=tranquility&size=128)

## Inventory Types
* URL Pattern: `/types/{typeID}/icon?tenant={tenant}&size={size}`
* Available Sizes: 32, 64, 128, 256, 512 and 1024
* Samples:
    * [Domination Stasis Webifier](https://images.evetech.net/types/14264/icon?tenant=tranquility&size=64)
    * [Exotic Dancers](https://images.evetech.net/types/17765/icon?tenant=tranquility&size=64)

## Ship and Drone Renders
* URL Pattern: `/types/{typeID}/render?tenant={tenant}&size={size}`
* Available Sizes: 32, 64, 128, 256, 512 and 1024
* Samples:
    * [Machariel](https://images.evetech.net/types/17738/render?tenant=tranquility&size=512)
    * [Firbolg](https://images.evetech.net/types/23059/render?tenant=tranquility&size=128)


# Legacy Portraits
Legacy portraits are from before the change to the existing character creator that occurred on November 30th, 2010 with the release of the Incursion expansion. These renders let you see how characters that existed back then looked in the previous character creator.

* [Old Character Portraits](http://cdn1.eveonline.com/data/OldCharPortraits_256.zip)
