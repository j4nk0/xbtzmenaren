from decimal import Decimal as Dec
from .models import Order_buy_btc, Order_sell_btc, Order_buy_ltc, Order_sell_ltc

def D(flt):
    return Dec(str(flt))
    
def get_rid_of_trailing_zeros(n):
    res = n
    for i in range(10, -1, -1):
        new_res = n.quantize(D(0.1) ** D(i))
        if new_res != n: break
        res = new_res
    return res

def r(x):
    return get_rid_of_trailing_zeros(x)

def preview_market_buy_btc(sum_eur):
    sum_eur = D(sum_eur)
    sum_btc = 0
    for order in Order_sell_btc.objects.all().order_by('price'):
        if order.btc * order.price > sum_eur:
           sum_btc += sum_eur / order.price
           break
        else:
            sum_eur -= order.btc * order.price
            sum_btc += order.btc
    return r(sum_btc)

def price_market_sell_btc(sum_btc):
    sum_btc = D(sum_btc)
    old_sum_btc = sum_btc
    sum_eur = 0
    for order in Order_buy_btc.objects.all().order_by('-price'):
        if order.btc > sum_btc:
            sum_eur += sum_btc * order.price
            break
        else:
            sum_btc -= order.btc
            sum_eur += order.btc * order.price
    return r(sum_eur / old_sum_btc)

def price_market_buy_ltc(sum_eur):
    sum_eur = D(sum_eur)
    old_sum_eur = sum_eur
    sum_ltc = 0
    for order in Order_sell_ltc.objects.all().order_by('price'):
        if order.ltc * order.price > sum_eur:
           sum_ltc += sum_eur / order.price
           break
        else:
            sum_eur -= order.ltc * order.price
            sum_ltc += order.ltc
    return r(old_sum_eur / sum_ltc)

def price_market_sell_ltc(sum_ltc):
    sum_ltc = D(sum_btc)
    old_sum_ltc = sum_ltc
    sum_eur = 0
    for order in Order_buy_ltc.objects.all().order_by('-price'):
        if order.ltc > sum_ltc:
            sum_eur += sum_ltc * order.price
            break
        else:
            sum_ltc -= order.ltc
            sum_eur += order.ltc * order.price
    return r(sum_eur / old_sum_ltc)

def rates():
    res = {
        'BTC-EUR': {
             'buy': str(r(Order_sell_btc.objects.all().order_by('price')[0].price)),
             'sell': str(r(Order_buy_btc.objects.all().order_by('-price')[0].price)),
        },
        'LTC-EUR': {
             'buy': str(r(Order_sell_ltc.objects.all().order_by('price')[0].price)),
             'sell': str(r(Order_buy_ltc.objects.all().order_by('-price')[0].price)),
        }
    }
    return res

def fee_market_buy_btc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    return fee

