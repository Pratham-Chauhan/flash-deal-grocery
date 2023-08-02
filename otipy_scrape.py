import pdb
import requests
import json
from time import sleep
import pandas as pd
import os.path
from datetime import datetime

saved_location = './Flash_deal_product_list.csv'
if os.path.exists(saved_location):
    FD = pd.read_csv(saved_location)
else:
    column = ['ID', 'Start_time', 'End_time', 'Start_time_String',
              'End_time_string', 'Item', 'Quantity', 'Price', 'Normal Price', 'Diff.']
    FD = pd.DataFrame(columns=column)


def extract_info(i):
    price = i['price']  # Limited Price

    start_time, end_time = i['start_time'], i['end_time']
    start_time_string = datetime.fromtimestamp(start_time)
    end_time_string = datetime.fromtimestamp(end_time)

    prod = i['normal_product']
    id = prod['id']
    # pdb.set_trace()
    if not FD.empty:
        for row in FD.to_numpy():
            if (id == row[0]) & (price == row[7]): 
                print('item already stored.', (id, start_time))
                return

    name, quantity, normal_price = prod['name'], prod['pack_qt'], prod['price']

    d = [id, start_time, end_time, start_time_string, end_time_string,
         name, quantity, price, normal_price, (normal_price-price)]
    # print("{:35s} | {:10s} | ₹{:5d} | ₹{:5d}".format(*d))
    FD.loc[len(FD)] = d


def scrape():
    headers = {
        'authority': 'gcptest.crofarm.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'access-token': 'e31306fb27e6172c8be9672ea7e95ee5a7eccb7a9b788d282d65a56ed91c3878',
        'client': 'web',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.otipy.com',
        'referer': 'https://www.otipy.com/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
        'feed_type': 'web',
        'latitude': '28.45170162',
        'longitude': '77.01849746',
    }

    x = requests.get('https://gcptest.crofarm.com/otipy/web/feed/v1/',
                     params=params, headers=headers)
    if x.status_code != 200:
        return

    jdata = x.json()['data']['widget_list']
    flash_deal = jdata[1]['data']['items']

    print('Flash Deal Items:', len(flash_deal))
    for item in flash_deal:
        extract_info(item)

for t in range(100):
    scrape()
    # print(FD)
    FD.to_csv(saved_location, index=False)

    print("Waiting 10 mins")
    sleep(10*60) # in mins
