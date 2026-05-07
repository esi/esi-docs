# TypeList as provided by the Static Data Export
@dataclass
class TypeList:
    includedTypeIDs: Optional[list[int]]    # TypeList data omits the field if it has no entries
    excludedTypeIDs: Optional[list[int]]
    includedGroupIDs: Optional[list[int]]
    excludedGroupIDs: Optional[list[int]]
    includedCategoryIDs: Optional[list[int]]
    excludedCategoryIDs: Optional[list[int]]

def typelist_contains(typelist: TypeList, item_typeid: int, item_groupid: int, item_categoryid: int):
    # Item is in any of the inclusions but not in none of the exclusions
    return (
        (typelist.includedCategoryIDs is not None and item_categoryid in typelist.includedCategoryIDs)
        or (typelist.includedGroupIDs is not None and item_groupid in typelist.includedGroupIDs)
        or (typelist.includedTypeIDs is not None and item_typeid in typelist.includedTypeIDs)
    ) and (
        (typelist.excludedCategoryIDs is None or item_categoryid not in typelist.excludedCategoryIDs)
        and (typelist.excludedGroupIDs is None or item_groupid not in typelist.excludedGroupIDs)
        and (typelist.excludedTypeIDs is None or item_typeid not in typelist.excludedTypeIDs)
    )