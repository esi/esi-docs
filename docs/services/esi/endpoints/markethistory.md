---
title: Market history
---
# Market history

[This endpoint](https://esi.evetech.net/ui/#/Market/get_markets_region_id_history) serves the regional markets' historical data statistics, per type.

## Response information

This paths returns the data from the Eve's monolith as-is, and therefore contains the same issues. Typically, `lowest` and `highest` are not the actual lowest and highest prices, but values tinkered by CCP's daily summarizing process. Those returned values can be very far from the actual ones, the actual way those values are created is not explained by CCP.

While the returned entries are usually sorted by date ASC, nothing in the specs enforces this, so this behaviour is not an actual rule. If you want to have the last or first data, you **should** sort them.

Days with no sale are not represented in the reponse, while they are present with a 0 volume in the game, assuming prior information exists.

The response does not contain today's value that is shown in-game. This value is indeed processed at the end of the next day. The response may not contain the previous day's values either, eg [Tritanium(34) in The Forge(10000002)](https://esi.evetech.net/latest/markets/10000002/history/?datasource=tranquility&type_id=34) may have values up to two days before.

## Limits

This path is specifically limited to 300 queries per IP per minute. Listing your future requests and only fetching as much as you can may be needed to avoid a ban.

This path returns a 404 when the region does not have a market, or does not have an actual history of sales for a type. Since daily records can be delayed up to 2 days, it means a new item (or an item barely sold) can return 404 up to two days after it's been sold. This makes the ability to discern which type to fetch the history in which region very difficult : An item with a SO offer and effectively sold after 30 days can have no history for a while, while still present in [the regional's types](https://esi.evetech.net/ui/#/Market/get_markets_region_id_types) and [the regional market](https://esi.evetech.net/ui/#/Market/get_markets_region_id_orders). This makes it especially hard to prefetch the data correctly.

## History

 - 2022-12 : [CCP Zelus explains the issues with that endpoint and why it's shut down](https://forums.eveonline.com/t/esi-market-history-endpoint/387151)
