import datetime
import requests
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

market_data = []

def fetch_ethereum_data():
    global market_data

    # Get the current date
    today = datetime.date.today()

    # Calculate the date from a year ago
    one_year_ago = today - datetime.timedelta(days=365)

    # Construct the Coingecko API URL
    api_url = f"https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=365"

    # Send a GET request to Coingecko API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Iterate over each data point
        for i in range(len(data['prices'])):
            # Extract the required fields from the response
            price = data['prices'][i][1]
            total_volume = data['total_volumes'][i][1]
            market_cap = data['market_caps'][i][1]
            last_updated = data['prices'][i][0]

            # Create a dictionary to store the market data for the current day
            current_day_data = {
                'date': datetime.datetime.fromtimestamp(last_updated / 1000).strftime('%Y-%m-%d'),
                'price': price,
                'total_volume': total_volume,
                'market_cap': market_cap,
                'last_updated': last_updated
            }

            # Check if the current day's data is already present in market_data
            existing_data = [d for d in market_data if d['date'] == current_day_data['date']]
            if not existing_data:
                # Add the market data for the current day to the list
                market_data.append(current_day_data)
    else:
        print('Failed to retrieve data from Coingecko API')

    # Reverse the market_data list to have the latest entry on top
    market_data = market_data[::-1]

# Call the fetch_ethereum_data() function initially to populate the market_data list
fetch_ethereum_data()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_ethereum_data, 'interval', days=1)
scheduler.start()

@app.route('/ethereum', methods=['GET'])
def get_ethereum_data():
    return jsonify(market_data)

if __name__ == '__main__':
    app.run(debug=True)
