import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
api_key = os.getenv('ALPHAVANTAGE_API_KEY')
currency = 'USD'
f = open('./data/investments.json')
inv_dict = json.load(f)

data = {}
for inv in inv_dict['investments']:
    d = {'date': [], 'price': []}
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol={inv['ticker']}&market={currency}&apikey={api_key}"
    r = requests.get(url)
    apiData = r.json()

    for key, value in apiData['Time Series (Digital Currency Monthly)'].items():
        date = datetime.strptime(key, '%Y-%m-%d')
        if date > datetime.strptime(inv['startDate'], '%Y-%m-%d'):
            d['date'].insert(0, datetime.strftime(date, '%m/%y'))
            d['price'].insert(0, float(value['4a. close (USD)']))
        else:
            break
    data[inv['ticker']] = d

with open('./data/data.json', 'w') as outfile:
    json.dump(data, outfile)


