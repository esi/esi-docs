<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

## Resolving Structure Markets

Structure market orders, with the exception of ranged orders, are not included in the results of `/markets/{region_id}/orders/`. They have to be queried individually and then merged.

### Query individual structure markets

The authenticated endpoint `/markets/structures/{structure_id}/` can be used to retrieve market orders for a single Upwell structure. It requires an access token that grants the scope `esi-markets.structure_markets.v1` for a character with docking access to the structure.

See [Resolve Structure IDs](/docs/scenarios/resolve_structure_ids.md) for information on how to get the IDs of Upwell structures.

The endpoint will return all orders in the structure, it does not support filtering by order type or type id.

Pay attention to the `X-Pages` header in the response, multiple requests with the `page` query parameter may be necessary to retrieve all orders.
