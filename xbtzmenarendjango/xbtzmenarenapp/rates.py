from decimal import Decimal as Dec
from .models import *
from django.db import transaction
from django.db.models import F
from django.utils import timezone

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

def rates():
    try:
        btc_buy = r(Order_sell_btc.objects.all().order_by('price')[0].price)
    except:
        btc_buy = 'X'
    try:
        btc_sell = r(Order_buy_btc.objects.all().order_by('-price')[0].price)
    except:
        btc_sell = 'X'
    try:
        ltc_buy = r(Order_sell_ltc.objects.all().order_by('price')[0].price)
    except:
        ltc_buy = 'X'
    try:
        ltc_sell = r(Order_buy_ltc.objects.all().order_by('-price')[0].price)
    except:
        ltc_sell = 'X'
    res = {
        'BTC-EUR': {
             'buy': btc_buy,
             'sell': btc_sell,
        },
        'LTC-EUR': {
             'buy': ltc_buy,
             'sell': ltc_sell,
        }
    }
    return res

#=======================BUYS========================================================================

def fee_market_buy_btc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def fee_market_buy_ltc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
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
    if fee > D(sum_eur): fee = D(sum_eur)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def fee_market_sell_ltc(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
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

#=======================LIMIT ORDER BUYS============================================================

def fee_limit_order_buy_btc(sum_eur):
    return D(0)

def fee_limit_order_buy_ltc(sum_eur):
    return D(0)

def preview_limit_order_buy_btc(sum_btc, price_btc):
    sum_eur = sum_btc * price_btc
    fee = r(fee_limit_order_buy_btc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def preview_limit_order_buy_ltc(sum_ltc, price_ltc):
    sum_eur = sum_ltc * price_ltc
    fee = r(fee_limit_order_buy_ltc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_buy_btc(user, sum_btc, price_btc):
    sum_eur = sum_btc * price_btc
    sum_eur_after_fees = sum_eur - fee_limit_order_buy_btc(sum_eur)
    sum_btc_after_fees = sum_eur_after_fees / price_btc
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(eur=F('eur') - sum_eur)
        if bal[0].eur < 0: raise ValueError
        Order_buy_btc.objects.create(
            user=user,
            btc=sum_btc_after_fees,
            price=price_btc,
            datetime=timezone.now()
        )

def limit_order_buy_ltc(user, sum_ltc, price_ltc):
    sum_eur = sum_ltc * price_ltc
    sum_eur_after_fees = sum_eur - fee_limit_order_buy_ltc(sum_eur)
    sum_ltc_after_fees = sum_eur_after_fees / price_ltc
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(eur=F('eur') - sum_eur)
        if bal[0].eur < 0: raise ValueError
        Order_buy_ltc.objects.create(
            user=user,
            ltc=sum_ltc_after_fees,
            price=price_ltc,
            datetime=timezone.now()
        )

def delete_limit_order_buy_btc(order_id):
    order = Order_buy_btc.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    sum_eur = order.btc * order.price
    with transaction.atomic():
        order.delete()
        bal.update(eur=F('eur') + sum_eur)

def delete_limit_order_buy_ltc(order_id):
    order = Order_buy_ltc.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    sum_eur = order.ltc * order.price
    with transaction.atomic():
        order.delete()
        bal.update(eur=F('eur') + sum_eur)

#=======================LIMIT ORDER SELLS===========================================================

def fee_limit_order_sell_btc(sum_eur):
    return D(0)

def fee_limit_order_sell_ltc(sum_eur):
    return D(0)

def preview_limit_order_sell_btc(sum_btc, price_btc):
    sum_eur = sum_btc * price_btc
    fee = r(fee_limit_order_sell_btc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def preview_limit_order_sell_ltc(sum_ltc, price_ltc):
    sum_eur = sum_ltc * price_ltc
    fee = r(fee_limit_order_sell_ltc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

