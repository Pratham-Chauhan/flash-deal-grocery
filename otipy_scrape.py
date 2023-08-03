import pdb
import os.path
import requests
import json

import pandas as pd
from datetime import datetime
from time import sleep, time

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

saved_location = './Flash_deal_product_list.csv'
if os.path.exists(saved_location):
    FD = pd.read_csv(saved_location)
else:
    column = ['ID', 'Start_time', 'End_time', 'Start_time_String',
              'End_time_string', 'Item', 'Quantity', 'Price', 'Normal Price', 'Diff.']
    FD = pd.DataFrame(columns=column)

current_deal_items = []
count = 0
def extract_info(i):
    global count, current_deal_items
    price = i['price']  # Limited Price
    
    # --TODO-- delete these start_time_string and end_time_string, also the columns from csv
    start_time, end_time = i['start_time'], i['end_time']
    start_time_string = datetime.fromtimestamp(start_time)
    end_time_string = datetime.fromtimestamp(end_time)

    prod = i['normal_product']
    id = prod['id']
    name, quantity, normal_price = prod['name'], prod['pack_qt'], prod['price']
    pdb.set_trace()  

    # -- TODO -- Urgent change, price need to be per kg, cause their price get changed with quantity weight
    # so what needs to be done is: price/prod['in_kg'] and also in excel, change price to per kg by using formula
    prod['pack_qt'], prod['in_kg']
    # print((name, price))
    # save all the items in current deal no matter price got changed or not
    current_deal_items.append(name)
    if not FD.empty:
        for row in FD.to_numpy():
            # Note: ID is no longer identify an Item, that means, one item can change its ID over time :(
            # if (name == row[5]) & (price == row[7]):
            if (start_time == row[1]) & (name == row[5]):
                # print('item already stored.', (id, name))
                return


    d = [id, start_time, end_time, start_time_string, end_time_string,
         name, quantity, price, normal_price, (normal_price-price)]
    # print("{:35s} | {:10s} | ₹{:5d} | ₹{:5d}".format(*d))
    FD.loc[len(FD)] = d
    count += 1

def scrape():
    global count
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
    if count == 0:
        print('No Update bro.')
    else:
        print(f'{count} items added & price changed.\n')


for t in range(1):
    # reset count and current-deal-items
    count, current_deal_items = 0, []

    scrape()
    # print(FD)
    FD.to_csv(saved_location, index=False)

    next_deal_time = FD['End_time_string'].iloc[-1]
    print('Come back at around %s'%next_deal_time)
    print("Waiting 10 mins")
    # sleep(10*60)  # in mins

# some insight from the data
df = FD
# Calculate discount percentage
df['Discount'] = (df['Diff.']/df['Normal Price'])*100
df['Discount'] = df.Discount.round(1)


# print(current_deal_items)
# Create beautiful graph for each items once done scraping
def create_graph():
    # play around on jupyter notebook for now
    current_time = int(time())
    current_time = datetime.fromtimestamp(current_time)
    
    plt.style.use('bmh')
    # fig = plt.figure(figsize=(15,6))

    for name in current_deal_items:
        df3 = df[df.Item == name] # filter each item by their name
        
        x = df3['Start_time'].apply(datetime.fromtimestamp).to_numpy()
        x = np.append(x, np.datetime64(current_time))

        y = df3['Price'].to_numpy()
        y = np.append(y, y[-1])

        y2 = df3['Normal Price'].to_numpy()
        y2 = np.append(y2, y2[-1])

        print("X : ", x,"\nY:", y)



        ''' Customize the style '''
        # Format the date ticks on the x-axis
        date_format = mdates.DateFormatter('%I:%M %p\n %b-%d ')  # Customize the format as per your preference
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=30)

        plt.grid(True, linestyle='--', linewidth=0.5)
        # plt.tick_params(axis='both', labelsize=18)  
        title = df3['Item'].iloc[0]
        plt.title(title)

        plt.step(x, y2, 'o-', where='post')
        plt.step(x, y, 'o-', where='post')
        
        # plt.show()
        plt.savefig(f'./img/{title}.png')
        plt.close()

#create_graph()

