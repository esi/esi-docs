import requests
import json
from threading import Thread,Lock
import pandas as pd
import argparse

# https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=buy&page=1
# https://esi.evetech.net/latest/markets/10000002/types/?datasource=tranquility&page=1
# x = requests.get('https://esi.evetech.net/latest/markets/10000002/types/?datasource=tranquility&page=20')
# json_object = json.loads(x.text)
# json_object.sort(key=lambda x: x['type_id'])


deskLock = Lock()


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--region", type=str, default="10000002")
parser.add_argument("--page", type=int, default=600)
args = parser.parse_args()

region = args.region
page = args.page
print(f"Starting{region}")
def group_json_by_field(data, field):
    grouped_data = {}
    for item in data:
        key = item[field]
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item)
    return grouped_data


def GetSellList(start, end, items):
    # x = requests.get('https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=sell&page=%d' % start)
    # items += json.loads(x.text)
    print(f"query page {start}")
    for i in range(start, end):
        headers = {'Connection': 'close'}
        x = requests.get(f'https://esi.evetech.net/latest/markets/{region}/orders/?datasource=tranquility&order_type=all&page={i}', headers=headers)
        if(x.status_code == 200):
            json_object = json.loads(x.text)
            deskLock.acquire()
            items += json_object
            deskLock.release()
    

items = []
page_stride = 2
threadingCount = int(page / page_stride) + 1
threadList = []
for i in range(0, threadingCount):
    thread = Thread(target=GetSellList, args = (page_stride * i + 1, page_stride * (i + 1) + 1, items))
    thread.start()
    threadList.append(thread)
for thread in threadList:
    thread.join()

# with open(f"region_all_{region}.json", "w") as outfile:
#     json.dump(items, outfile)
df = pd.DataFrame(items)
df.to_csv(f'region_all_{region}.csv', index=False)


# items_groups = group_json_by_field(items, 'type_id')

# min_price_items = []
# for key in items_groups:
#     min_price_items.append(items_groups[key].sort(key=lambda x: x['price']))
       
# print(min_price_items)




