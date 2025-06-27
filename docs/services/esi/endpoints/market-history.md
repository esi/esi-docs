---
title: Market history
---
# Market history

[This endpoint](https://esi.evetech.net/ui/#/Market/get_markets_region_id_history) serves the regional markets' historical data statistics, per type.

## Limits

This endpoint is specifically limited to 300 queries per IP per minute. Managing your requests as a whole, to enforce this limit on your end, may be needed to avoid a ban. 

This endpoint returns a 404 when the region does not have a market, or does not have an actual history of sales for a type. Since historical daily records can be delayed by up to 2 days, requesting an item with no previous sales memorized will return a 404 up to two days after an actual sale.  
This makes the ability to select the types for which to prefetch the history in a region very difficult : a type can be present in [the regional types](https://esi.evetech.net/ui/#/Market/get_markets_region_id_types) and be referenced in [the regional market](https://esi.evetech.net/ui/#/Market/get_markets_region_id_orders) , while still having no history in the corresponding region ; and later have an history entry while not being present in those endpoints.

## Response details

This path returns the data from the EVE's monolith as-is, and thus has the same issues. Typically, `lowest` and `highest` are not the actual lowest and highest prices, but values tinkered by CCP's daily summarizing process. Those "historical" lowest/highest values can be far from the actual ones. The way these values are created is not explained by CCP.

While the returned records are usually sorted by date ascending, nothing in the specs enforces this sort, so you should not rely on that behaviour. If you want to have the newest or oldest record, you **should** sort them first.

The days furing which no sale occured are not represented in the reponse, while they are present with a 0 volume in the game, assuming prior information exists.

The response does not contain today's value that is shown in-game. This value is indeed processed at the end of the next day. The response may not contain the previous day's values either, eg [Tritanium (34) in The Forge (10000002)](https://esi.evetech.net/latest/markets/10000002/history/?datasource=tranquility&type_id=34) may have values up to two days before now.

## History

 - 2022-12 : [CCP Zelus explains the issues with that endpoint and why it's shut down](https://forums.eveonline.com/t/esi-market-history-endpoint/387151)
