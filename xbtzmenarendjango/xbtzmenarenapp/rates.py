from decimal import Decimal as Dec
from .models import Order_buy_btc, Order_sell_btc, Order_buy_ltc, Order_sell_ltc
from .models import DECIMAL_PLACES_BTC, DECIMAL_PLACES_LTC, DECIMAL_PLACES_EUR

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

#=======================BUYS========================================================================

def fee_market_buy_btc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def fee_market_buy_ltc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def preview_market_buy_btc(sum_eur):
    sum_eur = D(sum_eur) - fee_market_buy_btc(sum_eur)
    sum_btc = 0
    for order in Order_sell_btc.objects.all().order_by('price'):
        if order.btc * order.price > sum_eur:
           sum_btc += sum_eur / order.price
           break
        else:
            sum_eur -= order.btc * order.price
            sum_btc += order.btc
    if sum_btc <= 0: return 0
    return r(sum_btc.quantize(D(0.1) ** DECIMAL_PLACES_BTC))

def preview_market_buy_ltc(sum_eur):
    sum_eur = D(sum_eur) - fee_market_buy_ltc(sum_eur)
    sum_ltc = 0
    for order in Order_sell_ltc.objects.all().order_by('price'):
        if order.ltc * order.price > sum_eur:
           sum_ltc += sum_eur / order.price
           break
        else:
            sum_eur -= order.ltc * order.price
            sum_ltc += order.ltc
    if sum_ltc <= 0: return 0
    return r(sum_ltc.quantize(D(0.1) ** DECIMAL_PLACES_LTC))

#=======================SELLS=======================================================================
def fee_market_sell_btc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def fee_market_sell_ltc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def preview_market_sell_btc(sum_btc):
    sum_btc = D(sum_btc)
    sum_eur = 0
    for order in Order_buy_btc.objects.all().order_by('-price'):
        if order.btc > sum_btc:
            sum_eur += sum_btc * order.price
            break
        else:
            sum_btc -= order.btc
            sum_eur += order.btc * order.price
    fee = r(fee_market_sell_btc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return (fee, sum_eur)

def preview_market_sell_ltc(sum_ltc):
    sum_ltc = D(sum_ltc)
    sum_eur = 0
    for order in Order_buy_ltc.objects.all().order_by('-price'):
        if order.ltc > sum_ltc:
            sum_eur += sum_ltc * order.price
            break
        else:
            sum_ltc -= order.ltc
            sum_eur += order.ltc * order.price
    fee = r(fee_market_sell_ltc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return (fee, sum_eur)

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


