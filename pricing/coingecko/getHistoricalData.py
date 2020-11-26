from pycoingecko import CoinGeckoAPI
cgapi = CoinGeckoAPI()

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

from datetime import datetime, timedelta

coins_list = [ coin['id'] for coin in cgapi.get_coins_list() ]

print(coins_list)
print(len(coins_list))

vs_currencies_list = cgapi.get_supported_vs_currencies()

print(vs_currencies_list)
print(len(vs_currencies_list))

time_to = datetime.now().timestamp()
time_from = (datetime.now() - timedelta(days=2)).timestamp()

data = cgapi.get_coin_market_chart_range_by_id('bitcoin', 'eur', time_from, time_to)

print(time_from)
print(time_to)
print(data)
