from pycoingecko import CoinGeckoAPI

cgapi = CoinGeckoAPI()

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

coins_list = [ coin['id'] for coin in cgapi.get_coins_list() ]

print(coins_list)
print(len(coins_list))

vs_currencies_list = cgapi.get_supported_vs_currencies()

print(vs_currencies_list)
print(len(vs_currencies_list))
