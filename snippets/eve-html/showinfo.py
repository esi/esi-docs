from typing import Callable, Optional

# Group and category IDs from the SDE (`groups.yaml` and `categories.yaml`).
GROUP_CHARACTER = 1
GROUP_CORPORATION = 2
GROUP_REGION = 3
GROUP_CONSTELLATION = 4
GROUP_SOLAR_SYSTEM = 5
GROUP_FACTION = 19
GROUP_ALLIANCE = 32

CATEGORY_CELESTIAL = 2
CATEGORY_STATION = 3
CATEGORY_STRUCTURE = 65

GROUP_ENTITIES = {
    GROUP_CHARACTER: "character",
    GROUP_CORPORATION: "corporation",
    GROUP_FACTION: "faction",
    GROUP_ALLIANCE: "alliance",
    GROUP_REGION: "region",
    GROUP_CONSTELLATION: "constellation",
    GROUP_SOLAR_SYSTEM: "solar_system",
}

CATEGORY_ENTITIES = {
    CATEGORY_CELESTIAL: "celestial",
    CATEGORY_STATION: "station",
    CATEGORY_STRUCTURE: "structure",
}


def parse_showinfo(
    href: str,
    group_of_type: Callable[[int], Optional[int]],
    category_of_group: Callable[[int], Optional[int]],
):
    """Resolve a `showinfo:` link into (entity kind, type ID, entity ID).

    `group_of_type` and `category_of_group` are lookups into the SDE (or the
    equivalent `/universe/types/` and `/universe/groups/` ESI routes).
    """
    if not href.lower().startswith("showinfo:"):
        return None

    # Segments after the second are not used by anything we know of, but
    # ignore them rather than rejecting the link.
    segments = href.split(":", 1)[1].split("//")
    if not segments[0].isdigit():
        return None
    type_id = int(segments[0])

    # A single segment is a link to the type itself, not to any one instance of it.
    if len(segments) == 1:
        return "type", type_id, None

    # Real data contains damaged links — `showinfo:2// 1000054` appears in the
    # SDE — so tolerate stray whitespace, but report a second segment that is
    # not a number rather than quietly downgrading the link to its type.
    entity = segments[1].strip()
    if not entity.isdigit():
        return "damaged", type_id, None
    entity_id = int(entity)

    # With two segments, the type ID only says what kind of thing the entity ID is.
    group_id = group_of_type(type_id)
    if group_id in GROUP_ENTITIES:
        return GROUP_ENTITIES[group_id], type_id, entity_id

    category_id = category_of_group(group_id) if group_id is not None else None
    if category_id in CATEGORY_ENTITIES:
        return CATEGORY_ENTITIES[category_id], type_id, entity_id

    # Anything else is an individual item of that type, such as a specific ship.
    return "item", type_id, entity_id
