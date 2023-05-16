import requests
from datetime import datetime, timedelta
def format_number(number):
    # Convert number to string and format with commas
    return "{:,}".format(number)
def get_historical_data(crypto_symbols, start_date, end_date):
    api_key = "b332c947-4e65-4464-8ac0-20e4647e0ac9"
    base_url = "https://min-api.cryptocompare.com/data/v2/histoday"

    historical_data = {}

    for symbol in crypto_symbols:
        url = f"{base_url}?fsym={symbol}&tsym=USD&limit=7&toTs={end_date}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        if "Data" in data:
            crypto_data = data["Data"]["Data"]
            historical_data[symbol] = crypto_data

    return historical_data

crypto_symbols = ["BTC", "ETH", "BNB", "XRP", "SOL"]
end_date = datetime.now().timestamp()
start_date = (datetime.now() - timedelta(days=7)).timestamp()

historical_data = get_historical_data(crypto_symbols, start_date, end_date)

for symbol, data in historical_data.items():
    print(f"{symbol} Data:")
    for entry in data:
        date = datetime.fromtimestamp(entry["time"]).strftime("%Y-%m-%d")
        close_price = entry["close"]
        
        
        
        print(f"Date: {date}\tClose Price: {close_price}\t")
        
        
     
    print()
