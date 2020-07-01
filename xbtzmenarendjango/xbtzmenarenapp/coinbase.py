import requests
from decimal import *
from time import sleep
from threading import Thread

#getcontext().prec = 10

btceur_spot = [Decimal(0)]
ltceur_spot = [Decimal(0)]

def download_btceur_spot_price():
    while True:
        response = requests.get('https://api.coinbase.com/v2/prices/BTC-EUR/spot')
        spot_price = Decimal(response.json()['data']['amount'])
        global btceur_spot
        btceur_spot.insert(0, spot_price)
        btceur_spot.pop()
        sleep(1)

Thread(target=download_btceur_spot_price, daemon=True).start()

def download_ltceur_spot_price():
    while True:
        response = requests.get('https://api.coinbase.com/v2/prices/LTC-EUR/spot')
        spot_price = Decimal(response.json()['data']['amount'])
        global ltceur_spot
        ltceur_spot.insert(0, spot_price)
        ltceur_spot.pop()
        sleep(1)

Thread(target=download_ltceur_spot_price, daemon=True).start()

def get_btceur_buy():
    buy_price = (btceur_spot[0] * Decimal('1.03')).quantize(Decimal('0.01'))
    return buy_price

def get_btceur_sell():
    sell_price = (btceur_spot[0] * Decimal('0.97')).quantize(Decimal('0.01'))
    return sell_price

def get_ltceur_buy():
    buy_price = (ltceur_spot[0] * Decimal('1.03')).quantize(Decimal('0.01'))
    return buy_price

def get_ltceur_sell():
    sell_price = (ltceur_spot[0] * Decimal('0.97')).quantize(Decimal('0.01'))
    return sell_price

