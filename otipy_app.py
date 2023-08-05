from flask import Flask, render_template
import otipy_scrape as otp

# print(otp.current_deal_items)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', menu_items=otp.current_deal_items)

if __name__ == '__main__':
    app.run(debug=True)
