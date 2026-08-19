# Reading SKINR Data

Players can create their own designs for ships: a hull plus a set of components (materials and patterns) placed in slots.
After sequencing one can obtain a license for these designs, to apply the design to your ship.

This guide covers how to read these designs, and their related data.

You need two sources:

- **ESI** tells you how a specific SKINR license looks like.
  The route is `/cosmetics/skinr/{skinr_id}`; try it in the [API Explorer](/api-explorer).
- **The [SDE](../services/static-data/index.md)** tells you what the IDs in that response mean.
  All the relevant files start with `skinr`.

## Slots

SKINR attributes have six visible parts: four materials and two patterns.
Each pattern also carries its own material, so there are eight slot IDs in total.
They live in `skinrSlots`, with internal names in `skinrSlotNames` and categories in `skinrSlotCategories`.

| Slot ID | Name                          | Internal name                | Category               |
|---------|-------------------------------|------------------------------|------------------------|
| 1       | Primary Slot                  | `primary_nanocoating`        | Material slot          |
| 2       | Secondary Slot                | `secondary_nanocoating`      | Material slot          |
| 3       | Detailing Slot                | `tertiary_nanocoating`       | Material slot          |
| 4       | Tech Slot                     | `tech_area`                  | Material slot          |
| 5       | Primary Pattern Slot          | `pattern`                    | Pattern slot           |
| 6       | Primary Pattern Material Slot | `pattern_material`           | Pattern material slot  |
| 7       | Secondary Pattern Slot        | `secondary_pattern`          | Pattern slot           |
| 8       | Secondary Pattern Material    | `secondary_pattern_material` | Pattern material slot  |

`allowedDesignComponentCategories` on each slot lists which component categories may go in it.
Material and pattern-material slots take `Material` and `Metallic` components; pattern slots take `Pattern` components.

Note: not every hull has all eight slots.
`skinrSlotConfigurations` decides that.

## Projection types

`projectionTypeU` and `projectionTypeV` on a pattern say what the renderer does when the texture runs out.
`U` and `V` are the two texture axes (horizontal and vertical), and they are set independently.

| Value             | Behavior outside the texture                                             |
|-------------------|--------------------------------------------------------------------------|
| `repeat`          | Start the texture over. Tiles forever.                                   |
| `clamp-to-edge`   | Stretch the last row/column of pixels outward. Smears the edge color.    |
| `clamp-to-border` | Draw nothing. The area outside the texture is transparent.               |

In practice: `repeat` gives you stripes that carry on around the hull, `clamp-to-border` gives you a decal that appears once, and `clamp-to-edge` sits in between.

## Slots to materials

Trinity, EVE's rendering engine, does not know about slots.
It describes a ship with four hull materials, `material1` to `material4`.
The four SKINR material slots have to be mapped onto these values.

The mapping depends on the **faction of the hull**, because the same physical area of an Amarr hull and a Caldari hull is authored as a different material index.
`skinrSlotsToMaterials` holds that mapping:

- `_key` is a `factionID`. Look it up in `factions`.
- `_value` is a list of `{slotID, materialID}` pairs, where `materialID` is the `N` in Trinity's `materialN`.

For the four empires:

| Slot | Amarr (500003) | Caldari (500001) | Gallente (500004) | Minmatar (500002) |
|------|----------------|------------------|-------------------|-------------------|
| 1    | `material4`    | `material3`      | `material4`       | `material4`       |
| 2    | `material1`    | `material2`      | `material3`       | `material3`       |
| 3    | `material2`    | `material4`      | `material1`       | `material2`       |
| 4    | `material3`    | `material1`      | `material2`       | `material1`       |

### Pattern projection

A pattern is not painted over the whole hull.
It is projected onto whichever material areas it is enabled for.
The ESI response expresses this as four booleans, `slot1` to `slot4`, in `configuration.pattern.configuration.projection`.

Those are **slot** numbers, not Trinity's material numbers.
So make sure to map those too when working with Trinity.
