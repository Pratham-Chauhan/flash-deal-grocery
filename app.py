from flask import Flask, render_template
import subprocess

# Create beautiful graph for each items and save them


def create_graph():

    print('reading data from csv...')
    df = pd.read_csv('Flash_deal_product_list.csv')
    # print(df.head().to_string())

    try:   # look for current item's name in the flash deal
        with open('items_list_current_deal.txt', 'r', encoding='utf-8') as f:
            current_deal_items = f.read().split('\n')
    except:
        current_deal_items = df['Item'].unique().tolist()

    current_time = int(time())
    current_time = datetime.fromtimestamp(current_time)

    plt.style.use('bmh')
    # fig = plt.figure(figsize=(15,6))
    for name in current_deal_items:
        df3 = df[df.Item == name]  # filter each item by their name

        x = df3['Start_time'].apply(datetime.fromtimestamp).to_numpy()
        x = np.append(x, np.datetime64(current_time))

        y = df3['Price per kg'].to_numpy()
        y = np.append(y, y[-1])

        y2 = df3['Normal Price per kg'].to_numpy()
        y2 = np.append(y2, y2[-1])

        # print("X : ", x,"\nY:", y)

        ''' Customize the style '''
        # Format the date ticks on the x-axis
        # Customize the format as per your preference
        date_format = mdates.DateFormatter('%I:%M %p\n %b-%d ')
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=30)

        plt.grid(True, linestyle='--', linewidth=0.5)
        # plt.tick_params(axis='both', labelsize=18)
        title = df3['Item'].iloc[0]
        plt.title(title)

        plt.step(x, y2, '-', where='post')
        plt.step(x, y, '-', where='post')

        # plt.show()
        # plt.close()

        # Save the image
        plt.savefig(f'./static/img/{title}.png')

    return current_deal_items


# run scraping process in backgroud
print('Running scraping script in new process...')
subprocess.Popen(["python3", "otipy_scrape.py"])

# print(create_graph())
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html', menu_items=create_graph())
