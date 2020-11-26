import requests
from time import sleep
from decimal import Decimal

spot_prices = []
while len(spot_prices) < 3600:
    response = requests.get('https://api.coinbase.com/v2/prices/BTC-EUR/spot')
    spot_price = Decimal(response.json()['data']['amount'])
    spot_prices.append(spot_price)
    sleep(1)
same_price_seconds = [1]
j = 0
pricej = spot_prices[0]
for i in range(1, len(spot_prices)):
    if spot_prices[i] == pricej:
        same_price_seconds[j] += 1
    else:
        same_price_seconds.append(1)
        j += 1
        pricej = spot_prices[i]
print('Price stays the same for at least ' + str(min(same_price_seconds[1:-1])) + ' seconds')
print('intervals in seconds: ' + str(same_price_seconds))
print('Prices: ' + str(spot_prices))
