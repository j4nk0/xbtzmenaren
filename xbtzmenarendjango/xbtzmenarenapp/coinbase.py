import requests
from decimal import *

getcontext().prec = 10

response = requests.get('https://api.coinbase.com/v2/prices/LTC-EUR/spot')
spot_price = Decimal(response.json()['data']['amount'])
buy_price = (spot_price * Decimal('1.03')).quantize(Decimal('0.01'))
print(buy_price)
