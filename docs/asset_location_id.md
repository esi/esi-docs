
## Asset `location_id` quick reference

- `item_id` of the parent asset (Used to build the assets tree, see example below)
- **Item ID of the active ship in space**
If the active ship is in space, the fitting, but, not the ship itself will be returned by the asset endpoint
You can get the active ship by combining data from following endpoints:
  - [ESI location endpoint](https://esi.evetech.net/ui/#/Location/get_characters_character_id_location)
  - [ESI ship endpoint](https://esi.evetech.net/ui/#/Location/get_characters_character_id_ship)
- **Asset Safty** (`location_id` == 2004)
- **System ID** (Range: 30000000 - 32000000)
- **Abyssal System ID** (Range: 32000000 - 33000000)
- **Station ID** (Range: 60000000 - 64000000)
- **Structure ID**
Resolvable via:
  - The [ESI structure endpoint](https://esi.evetech.net/ui/#/Universe/get_universe_structures_structure_id) (if you have docking rights)
  - The [ESI bookmark endpoint](https://esi.evetech.net/ui/#/Bookmarks/get_characters_character_id_bookmarks) (all structures you have bookmarked, resolve structures regardless of docking rights)
- **Customs Office ID** (Those are not resolvable, see [ESI feature request](https://github.com/esi/esi-issues/issues/685), Note: they share ID range with Item IDs and Structure IDs)
- **Character ID** (when `location_flag` is `wardrobe`)
- **Corporation Office ID** (Not resolvable, when `location_flag` is `OfficeFolder`, link between Hangars/Divisions (`location_flag`: `CorpSAGx`) and Structure/Station ID's.)

### Asset Tree example

#### Flat List
- item_id: 1000000000001, location_id: 60002959
- item_id: 1000000000002, location_id: 60002959
- item_id: 1000000000003, location_id: 1000000000001
- item_id: 1000000000004, location_id: 1000000000003
- item_id: 1000000000005, location_id: 1000000000003
#### Tree
- item_id: 1000000000001, location_id: 60002959
  - item_id: 1000000000003, location_id: 1000000000001
    - item_id: 1000000000004, location_id: 1000000000003
    - item_id: 1000000000005, location_id: 1000000000003
- item_id: 1000000000002, location_id: 60002959


### Fixed Bugs (only relevant for historic data)
- Returned destroyed assets ([ESI Issue](https://github.com/esi/esi-issues/issues/698))
- Returned 9e18 locations ([ESI Issue](https://github.com/esi/esi-issues/issues/684))
- Returned trained skills and active boosters ([ESI Issue](https://github.com/esi/esi-issues/issues/911))
- Returned  PI structures [ESI Issue](https://github.com/esi/esi-issues/issues/943)
