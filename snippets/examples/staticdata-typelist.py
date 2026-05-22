from dataclasses import dataclass
from typing import Optional


@dataclass
class TypeList:
    # TypeList data only includes fields with values, unset inclusion/exclusion lists act as if they were empty lists
    includedTypeIDs: Optional[list[int]]
    excludedTypeIDs: Optional[list[int]]
    includedGroupIDs: Optional[list[int]]
    excludedGroupIDs: Optional[list[int]]
    includedCategoryIDs: Optional[list[int]]
    excludedCategoryIDs: Optional[list[int]]
    # Additional fields not used in this example
    name: str
    displayName: Optional[str]
    displayDescription: Optional[str]


# Check whether a single type is contained in the typelist
# To do so the type_id, group_id, and category_id of the item must be known
def typelist_contains(typelist: TypeList, item_typeid: int, item_groupid: int, item_categoryid: int):
    # Precedence in order of excludes > includes, and types > groups > categories
    return (
            (
                    (
                            (
                                    (typelist.includedCategoryIDs is not None and item_categoryid in typelist.includedCategoryIDs)
                                    and (typelist.excludedCategoryIDs is None or item_categoryid not in typelist.excludedCategoryIDs)
                            ) or (typelist.includedGroupIDs is not None and item_groupid in typelist.includedGroupIDs)
                    ) and (typelist.excludedGroupIDs is None or item_groupid not in typelist.excludedGroupIDs)
            ) or (typelist.includedTypeIDs is not None and item_typeid in typelist.includedTypeIDs)
    ) and (typelist.excludedTypeIDs is None or item_typeid not in typelist.excludedTypeIDs)


# Prepare re-usable lookup tables
category_groups: dict[int, list[int]] = dict()  # For each categoryID, a list of the groupIDs in that category
group_types: dict[int, list[int]] = dict()      # For each groupID, a list of the typeIDs in that group


# Convert a TypeList into a set of typeIDs
def typelist_flatten(typelist: TypeList):
    list_categories = set()
    # 1) Add all included categories
    if typelist.includedCategoryIDs is not None:
        list_categories.update(typelist.includedCategoryIDs)
    # 2) Remove all excluded categories
    if typelist.excludedCategoryIDs is not None:
        list_categories.difference_update(typelist.excludedCategoryIDs)

    # 3) For each remaining category, retrieve it's groupIDs, and add these to a single set
    list_groups = {group_id for category_id in list_categories for group_id in category_groups.get(category_id, [])}
    # 4) Add includedGroupIDs to the set of groups
    if typelist.includedGroupIDs is not None:
        list_groups.update(typelist.includedGroupIDs)
    # 5) Remove excludedGroupIDs from the set of groups; Any group added in steps 3 or 4 that is in `excludedGroupIDs` is removed from the set
    if typelist.excludedGroupIDs is not None:
        list_groups.difference_update(typelist.excludedGroupIDs)

    # 6) For each remaining group, retrieve it's typeIDs, and add these to a single set
    list_types = {type_id for group_id in list_groups for type_id in group_types.get(group_id, [])}
    # 7) Add includedTypeIDs to the set of types
    if typelist.includedTypeIDs is not None:
        list_types.update(typelist.includedTypeIDs)
    # 8) Remove excludedTypeIDs from the set of types; Any type added in steps 6 or 7 that is in `excludedTypeIDs` is removed from the set
    if typelist.excludedTypeIDs is not None:
        list_types.difference_update(typelist.excludedTypeIDs)

    # 9) Done
    # The resulting set can now be used for efficiently checking if a type is contained in the typelist (`typeID in list_types`) or be iterated
    return list_types
