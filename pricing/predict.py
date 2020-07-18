import requests
from datetime import datetime, timedelta
from decimal import Decimal as Dec

def D(flt):
    return Dec(str(flt))
    
def get_max_delta_up(json, day):
    if day +1 == len(json): return D(json[day][2])- D(json[day][3])
    elif day + 2 == len(json): return max(D(json[day][2]), D(json[day +1][2])) - D(json[day][3])
    else: return max(D(json[day][2]), D(json[day +1][2]), D(json[day +2][2])) - D(json[day][3])

def get_max_delta_down(json, day):
    if day +1 == len(json): return D(json[day][3]) - D(json[day][1])
    elif day + 2 == len(json): return D(json[day][3]) - min(D(json[day][1]), D(json[day +1][1]))
    else: return D(json[day][3]) - min(D(json[day][2]), D(json[day +1][2]), D(json[day +2][2]))

def get_prediction(coin):
    start_time = (datetime.utcnow() - timedelta(days=10)).replace(microsecond=0)
    end_time = datetime.utcnow().replace(microsecond=0)
    URL = 'https://api.pro.coinbase.com/products/' + coin + '-EUR/candles?start='    \
         + start_time.isoformat() + '&end=' + end_time.isoformat() + '&granularity=86400'
    response = requests.get(URL)
    json = response.json()
    json.reverse()
    delta_ups = []
    delta_downs = []
    for day in range(len(json)):
        delta_ups.append(get_max_delta_up(json, day))
        delta_downs.append(get_max_delta_down(json, day))
    delta_up = max(delta_ups)
    delta_down = max(delta_downs)
    close = D(json[-1][4])
    print(coin)
    print(close)
    print(close + delta_up)
    print(close - delta_down)

get_prediction('BTC')
get_prediction('LTC')
