import requests
from datetime import datetime, timedelta
from decimal import Decimal as Dec

def D(flt):
    return Dec(str(flt))

def get_buy_amount_of_btc(amount_eur, asks):
    amount_eur = D(amount_eur)
    amount_btc = 0
    for ask in asks:
        if D(ask[0]) * D(ask[1]) < amount_eur:
            amount_eur -= D(ask[0]) * D(ask[1])
            amount_btc += D(ask[1])
        else:
            amount_btc += amount_eur / D(ask[0])
            break
    return amount_btc

def get_buy_amount(amount_btc, asks):
    amount_btc = D(amount_btc)
    amount_eur = 0
    for ask in asks:
        if D(ask[1]) < amount_btc:
            amount_btc -= D(ask[1])
            amount_eur += D(ask[0]) * D(ask[1])
        else:
            amount_eur += D(ask[0]) * amount_btc
            break
    return amount_eur

def get_sell_amount(amount_btc, bids):
    amount_btc = D(amount_btc)
    amount_eur = 0
    for bid in bids:
        if D(bid[1]) < amount_btc:
            amount_btc -= D(bid[1])
            amount_eur += D(bid[0]) * D(bid[1])
        else:
            amount_eur += D(bid[0]) * amount_btc
            break
    return amount_eur

URL = 'https://api.pro.coinbase.com/products/BTC-EUR/book?level=2'
response = requests.get(URL)
json = response.json()
print(json['bids'])
print(get_buy_amount(0.1, json['asks']))
print(get_buy_amount(1, json['asks']))
print(get_sell_amount(1, json['bids']))
print(get_buy_amount_of_btc(8133, json['asks']))
print(get_buy_amount_of_btc(500, json['asks']))
