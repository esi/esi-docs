# Understanding the EVE Online Image Service

## Introduction

The **EVE Online Image Service**, formerly known as the *image server*, functions as a reliable repository hosting a diverse array of images for various elements within the EVE Online game universe.

To access the service, visit [https://images.evetech.net/](https://images.evetech.net/).

## Image Categories and Structure

The URLs for images adhere to a specific pattern (Note: Replace the curly braces({}) and content within with actual values):
- `https://images.evetech.net/{category}/{id}/{variation}?{query}`

**Categories:**
- `alliances`
- `corporations`
- `characters`
- `types`

**Variations:**
  - For alliances and corporations: `logo`
  - For characters: `portrait`
  - Types may have different versions, which you can explore by checking `https://images.evetech.net/{category}/{id}` and reviewing a list provided in JSON format.

## Query Parameters

The service supports two key query parameters:

- **Size (`size`):**
  - Acceptable values: 32, 64, 128, 256, 512, and 1024.
  - If not specified, the image will be displayed in its original size.
 
   Example: `size=32`

- **Tenant (`tenant`):**
  - Determines the server for image requests.
  - The default is `tranquility`, and it also works with `singularity`.
 
   Example: `tenant=tranquility`

Remember that all query parameters are to be in `key=value` format and delimited with an ampersand(`&`).

   Example: `size=32&tenant=tranquility`

## Additional Details

- **NPC Faction Logos:**
  - Obtainable using the faction ID within the corporations category.

- **Default Logos/Portraits:**
  - ID 1 is a common identifier for alliances, corporations, and characters to retrieve the default logo or portrait.

- **Image Formats:**
  - Most images are in PNG format, except for character portraits, which are in JPEG format.

- **Usage Guidance:**
  - Think of the service as a CDN (Content Delivery Network); you don't need to store or provide the images yourself.

## Usage Examples

### Alliances

- [https://images.evetech.net/alliances/434243723](https://images.evetech.net/alliances/434243723)
  - Logo: [https://images.evetech.net/alliances/434243723/logo](https://images.evetech.net/alliances/434243723/logo)

### Corporations

- [https://images.evetech.net/corporations/109299958](https://images.evetech.net/corporations/109299958)
  - Logo: [https://images.evetech.net/corporations/109299958/logo](https://images.evetech.net/corporations/109299958/logo)

### NPC Factions

- [https://images.evetech.net/corporations/500001](https://images.evetech.net/corporations/500001)
  - Logo: [https://images.evetech.net/corporations/500001/logo](https://images.evetech.net/corporations/500001/logo)

### Characters

- [https://images.evetech.net/characters/1338057886](https://images.evetech.net/characters/1338057886)
  - Portrait: [https://images.evetech.net/characters/1338057886/portrait](https://images.evetech.net/characters/1338057886/portrait)

### Type - Rifter

- [https://images.evetech.net/types/587](https://images.evetech.net/types/587)
  - Icon: [https://images.evetech.net/types/587/icon](https://images.evetech.net/types/587/icon)
  - Render: [https://images.evetech.net/types/587/render](https://images.evetech.net/types/587/render)

### Type - 250mm Railgun II

- [https://images.evetech.net/types/3082](https://images.evetech.net/types/3082)
  - Icon: [https://images.evetech.net/types/3082/icon](https://images.evetech.net/types/3082/icon)

### Type - Avatar Blueprint

- [https://images.evetech.net/types/11568](https://images.evetech.net/types/11568)
  - Blueprint: [https://images.evetech.net/types/11568/bp](https://images.evetech.net/types/11568/bp)
  - Blueprint Copy: [https://images.evetech.net/types/11568/bpc](https://images.evetech.net/types/11568/bpc)

### Type - Intact Hull Section

- [https://images.evetech.net/types/30752](https://images.evetech.net/types/30752)
  - Relic: [https://images.evetech.net/types/30752/relic](https://images.evetech.net/types/30752/relic)

## Legacy Portraits

Legacy portraits showcase the visual history before the character creator's change on November 30th, 2010, aligning with the Incursion expansion. Explore these historical images: [Old Character Portraits](http://cdn1.eveonline.com/data/OldCharPortraits_256.zip).