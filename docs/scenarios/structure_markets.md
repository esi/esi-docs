## Resolving Structure Markets

Structure market orders, with the exception or ranged orders, are not included in the results of `/markets/{region_id}/orders/`. They have to be queried individually and then merged.

### Query individual structure markets

The authenticated endpoint `/markets/structures/{structure_id}/` can be used to retrieve market orders for a single Upwell structure. It requires an access token that grants the scope `esi-markets.structure_markets.v1` for a character with docking access to the structure.

See [Resolve Structure IDs](/docs/scenarios/resolve_structre_ids.md) for information on how to get the IDs of Upwell structures.

The endpoint will return all orders in the structure, it does not support filtering by order type or type id.

Pay attention to the `X-Pages` header in the response, multiple requests with the `page` query parameter may be necessary to retrieve all orders.