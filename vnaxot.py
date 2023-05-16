import requests
from datetime import datetime, timedelta
import pyodbc

server = '192.164'
database = 'test'
username = 'sa'
password = 'Sqd'


def format_number(number):
    # Convert number to string and format with commas
    return "{:,}".format(number)


def get_historical_data(crypto_symbols, start_date, end_date):
    api_key = ""
    base_url = "https://min-api.cryptocompare.com/data/v2/histoday"

    historical_data = {}
# aq ucvli 120  tveze ramdenic ginda imis mixedvitt
    for symbol in crypto_symbols:
        url = f"{base_url}?fsym={symbol}&tsym=USD&limit=120&toTs={end_date}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        if "Data" in data:
            crypto_data = data["Data"]["Data"]
            historical_data[symbol] = crypto_data

    return historical_data


def get_current_data(crypto_symbols):
    api_key = "b332c947-4e65-4464-8ac0-20e"
    base_url = "https://min-api.cryptocompare.com/data/pricemultifull"

    current_data = {}

    for symbol in crypto_symbols:
        url = f"{base_url}?fsyms={symbol}&tsyms=USD&api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        if "RAW" in data and symbol in data["RAW"]:
            crypto_data = data["RAW"][symbol]["USD"]
            current_data[symbol] = crypto_data

    return current_data


crypto_symbols = ["BTC", "ETH", "BNB", "XRP", "SOL"]
end_date = int(datetime.now().timestamp())
start_date = int((datetime.now() - timedelta(days=120)).timestamp())        #da aqac cvli 120 tveebis mixedvit 

historical_data = get_historical_data(crypto_symbols, start_date, end_date)
current_data = get_current_data(crypto_symbols)

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)
cursor = conn.cursor()

# Create the crypto table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE crypto (
#         id INTEGER PRIMARY KEY IDENTITY(1,1),
#         symbol TEXT,
#         date DATE,
#         close_price FLOAT,  -- or DECIMAL(18, 6),
#         market_cap FLOAT,  -- or DECIMAL(18, 6),
#         volume FLOAT,  -- or DECIMAL(18, 6)
#     )
# ''')

for symbol, data in historical_data.items():
    for entry in data:
        date = datetime.fromtimestamp(entry["time"]).strftime("%Y-%m-%d")
        close_price = entry["close"]

        if symbol in current_data:
            market_cap = current_data[symbol]["MKTCAP"]
            volume = current_data[symbol]["TOTALVOLUME24HTO"]
        else:
            market_cap = None
            volume = None

        # Insert the data into the crypto table
                
        cursor.execute('''
            INSERT INTO crypto (symbol, date, close_price, market_cap, volume)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, date, close_price, market_cap, volume))

# Commit the changes and close the connection
conn.commit()
conn.close()
print('successful')

