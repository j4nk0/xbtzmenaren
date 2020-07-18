import requests
from datetime import datetime, timedelta
from decimal import Decimal as Dec
from time import sleep
from threading import Thread
import json

btceur_rates = {
    'buy': Dec('100000'),
    'sell': Dec('0'),
}

ltceur_rates = {
    'buy': Dec('100000'),
    'sell': Dec('0'),
}

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

def get_eur_deltas(coin):
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
    delta = {
        'up': max(delta_ups),
        'down': max(delta_downs),
    }
    return delta

def get_buy_amount(amount_btc, asks):
    amount_btc = D(amount_btc)
    amount_eur = D(0)
    for ask in asks:
        if D(ask[1]) < amount_btc:
            amount_btc -= D(ask[1])
            amount_eur += D(ask[0]) * D(ask[1])
        else:
            amount_eur += D(ask[0]) * amount_btc
            break
    return amount_eur

def get_eur_buy_price(coin):
    URL = 'https://api.pro.coinbase.com/products/' + coin + '-EUR/book?level=2'
    response = requests.get(URL)
    json = response.json()
    return get_buy_amount(0.001, json['asks']) * D(1000)

def update_prices(last_price, delta, eur_rates):
    buy = max(last_price + delta['up'], last_price * D(1.02))
    sell = min(last_price - delta['down'], last_price * D(0.98))
    new_rates = {
        'buy': buy,
        'sell': sell
    }
    eur_rates.update(new_rates)

def check_rates_continuously():
    # check prices every 28 seconds
    global btceur_rates
    global ltceur_rates
    while True:
        btc_delta = get_eur_deltas('BTC')
        sleep(1)
        ltc_delta = get_eur_deltas('LTC')
        sleep(1)
        btc_last_price = get_eur_buy_price('BTC')
        sleep(1)
        ltc_last_price = get_eur_buy_price('LTC')
        update_prices(btc_last_price, btc_delta, btceur_rates)
        update_prices(ltc_last_price, ltc_delta, ltceur_rates)
        sleep(25)

Thread(target=check_rates_continuously, daemon=True).start()

# outputs:
def get_btceur_buy():
    return btceur_rates['buy']

def get_btceur_sell():
    return btceur_rates['sell']

def get_ltceur_buy():
    return ltceur_rates['buy']

def get_ltceur_sell():
    return ltceur_rates['sell']

def rates():
    res = {
        'BTC-EUR': {
             'buy': str(btceur_rates['buy']),
             'sell': str(btceur_rates['sell']),
        },
        'LTC-EUR': {
             'buy': str(ltceur_rates['buy']),
             'sell': str(ltceur_rates['sell']),
        }
    }
    return json.dumps(res)
