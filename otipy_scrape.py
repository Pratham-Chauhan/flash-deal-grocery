import requests
import json
import pandas as pd
import os.path
from datetime import datetime

saved_location = './Flash_deal_product_list.csv'
if os.path.exists(saved_location):
    FD = pd.read_csv(saved_location)
else:
    FD = pd.DataFrame(columns=['Item','Quantity', 'Price', 'Normal Price'])


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


def extract_info():
    x = requests.get('https://gcptest.crofarm.com/otipy/web/feed/v1/', params=params, headers=headers)

    if x.status_code != 200: return 

    jdata = x.json()['data']['widget_list']
    flash_deal = jdata[1]['data']['items']

    print('Flash Deal Items:', len(flash_deal))
    # print("{:35s} | {:10s} | {:5s} | {:5s}".format(FD.columns))
    for prod in flash_deal:
        price = prod['price']
        id = prod['prod_id']
        
        start_time = prod[1690615869]
        end_time = prod[1690826340]

        # normal product details
        prod = prod['normal_product']
        name = prod['name']
        quantity = prod['pack_qt']
        normal_price = prod['price']

        d = [name, quantity, price, normal_price]
        # print("{:35s} | {:10s} | ₹{:5d} | ₹{:5d}".format(*d))
        FD.loc[len(FD)] = d

extract_info()
print(FD)

FD.to_csv(saved_location)









