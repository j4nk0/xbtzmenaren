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
    try:
        doge_buy = r(Order_sell_doge.objects.all().order_by('price')[0].price)
    except:
        doge_buy = 'X'
    try:
        doge_sell = r(Order_buy_doge.objects.all().order_by('-price')[0].price)
    except:
        doge_sell = 'X'
    res = {
        'BTC-EUR': {
             'buy': btc_buy,
             'sell': btc_sell,
        },
        'LTC-EUR': {
             'buy': ltc_buy,
             'sell': ltc_sell,
        },
        'DOGE-EUR': {
             'buy': doge_buy,
             'sell': doge_sell,
        }
    }
    return res

#=======================BUYS========================================================================

def fee_market_buy(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))


for c in CURRENCIES:
    exec('''
def fee_market_buy_''' + c + '''(sum_eur):
    return fee_market_buy(sum_eur)

def preview_market_buy_''' + c + '''(sum_eur):
    sum_eur = D(sum_eur) - fee_market_buy_btc(sum_eur)
    sum_''' + c + ''' = 0
    for order in Order_sell_''' + c + '''.objects.all().order_by('price'):
        if order.''' + c + ''' * order.price > sum_eur:
           sum_''' + c + ''' += sum_eur / order.price
           break
        else:
            sum_eur -= order.''' + c + ''' * order.price
            sum_''' + c + ''' += order.''' + c + '''
    if sum_''' + c + ''' <= 0: return 0
    return r(sum_''' + c + '''.quantize(D(0.1) ** ''' + DECIMAL_PLACES[c] + '''))

def market_buy_''' + c + '''(user, sum_eur):
    sum_eur_before_fees = D(sum_eur)
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(eur=F('eur') - D(sum_eur))
        if bal.eur < 0: raise ValueError('Not enough funds')
        Order_sell_''' + c + '''.objects.all().select_for_update()
        sum_eur = D(sum_eur) - fee_market_buy_''' + c + '''(sum_eur)
        sum_''' + c + ''' = 0
        for order in Order_sell_''' + c + '''.objects.all().order_by('price'):
            if order.''' + c + ''' * order.price >= sum_eur:
                sum_''' + c + ''' += sum_eur / order.price
                order.''' + c + ''' -= sum_eur / order.price 
                order.save()
                if order.''' + c + ''' == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + sum_eur)
                break
            else:
                sum_eur -= order.''' + c + ''' * order.price
                sum_''' + c + ''' += order.''' + c + '''
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + order.''' + c + ''' * order.price)
        else:
            raise ValueError('Market order too big, not enough sell orders to accomodate')
        bal.update(''' + c + '''=F("''' + c + '''") + D(sum_''' + c + '''))
        Buy_''' + c + '''.objects.create(
            user=user,
            datetime=timezone.now(),
            ''' + c + '''=sum_''' + c + ''',
            eur=sum_eur_before_fees,
        )
''')

#=======================SELLS=======================================================================

def fee_market_sell(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

for c in CURRENCIES:
    exec('''
def fee_market_sell_''' + c + '''(sum_eur):
    return fee_market_sell(sum_eur)

def preview_market_sell_''' + c + '''(sum_''' + c + '''):
    sum_''' + c + ''' = D(sum_''' + c + ''')
    sum_eur = 0
    for order in Order_buy_''' + c + '''.objects.all().order_by('-price'):
        if order.''' + c + ''' > sum_''' + c + ''':
            sum_eur += sum_''' + c + ''' * order.price
            break
        else:
            sum_''' + c + ''' -= order.''' + c + '''
            sum_eur += order.''' + c + ''' * order.price
    fee = r(fee_market_sell_''' + c + '''(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return (fee, sum_eur)

def market_sell_''' + c + '''(user, sum_''' + c + '''):
    sum_''' + c + ''' = D(sum_''' + c + ''')
    original_sum_''' + c + ''' = sum_''' + c + '''
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(''' + c + '''=F("''' + c + '''") - sum_''' + c + ''')
        if bal.''' + c + ''' < 0: raise ValueError('Not enough funds')
        Order_buy_''' + c + '''.objects.all().select_for_update()
        sum_eur = 0
        for order in Order_buy_''' + c + '''.objects.all().order_by('-price'):
            if order.''' + c + ''' >= sum_''' + c + ''':
                sum_eur += sum_''' + c + ''' * order.price
                order.''' + c + ''' -= sum_''' + c + '''
                order.save()
                if order.''' + c + ''' == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(''' + c + '''=F("''' + c + '''") + sum_''' + c + ''')
                break
            else:
                sum_''' + c + ''' -= order.''' + c + '''
                sum_eur += order.''' + c + ''' * order.price
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(''' + c + '''=F("''' + c + '''") + order.''' + c + ''')
        else:
            raise ValueError('Market order too big, not enough buy orders to accomodate')
        sum_eur -= fee_market_sell_''' + c + '''(sum_eur)
        bal.update(eur=F('eur') + sum_eur)
        Sell_''' + c + '''.objects.create(
            user=user,
            datetime=timezone.now(),
            ''' + c + '''=original_sum_''' + c + ''',
            eur=sum_eur,
        )
''')

#=======================LIMIT ORDER BUYS============================================================

def fee_limit_order_buy(sum_eur):
    return D(0)
    
for c in CURRENCIES:
    exec('''
def fee_limit_order_buy_''' + c + '''(sum_eur):
    return fee_limit_order_buy(sum_eur)

def preview_limit_order_buy_''' + c + '''(sum_''' + c + ''', price_''' + c + '''):
    sum_eur = sum_''' + c + ''' * price_''' + c + '''
    fee = r(fee_limit_order_buy_''' + c + '''(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_buy_''' + c + '''(user, sum_''' + c + ''', price_''' + c + '''):
    try:
        if price_''' + c + ''' >= Order_sell_''' + c + '''.objects.all().order_by('price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_''' + c + ''' * price_''' + c + '''
    sum_eur_after_fees = sum_eur - fee_limit_order_buy_''' + c + '''(sum_eur)
    sum_''' + c + '''_after_fees = sum_eur_after_fees / price_''' + c + '''
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(eur=F('eur') - sum_eur)
        if bal[0].eur < 0: raise ValueError
        Order_buy_''' + c + '''.objects.create(
            user=user,
            ''' + c + '''=sum_''' + c + '''_after_fees,
            price=price_''' + c + ''',
            datetime=timezone.now()
        )

def delete_limit_order_buy_''' + c + '''(order_id):
    order = Order_buy_''' + c + '''.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    sum_eur = order.''' + c + ''' * order.price
    with transaction.atomic():
        order.delete()
        bal.update(eur=F('eur') + sum_eur)
''')

#=======================LIMIT ORDER SELLS===========================================================

def fee_limit_order_sell(sum_eur):
    return D(0)

for c in CURRENCIES:
    exec('''
def fee_limit_order_sell_''' + c + '''(sum_eur):
    return fee_limit_order_sell(sum_eur)

def preview_limit_order_sell_''' + c + '''(sum_''' + c + ''', price_''' + c + '''):
    sum_eur = sum_''' + c + ''' * price_''' + c + '''
    fee = r(fee_limit_order_sell_btc(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_sell_''' + c + '''(user, sum_''' + c + ''', price_''' + c + '''):
    try:
        if price_''' + c + ''' <= Order_buy_''' + c + '''.objects.all().order_by('-price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_''' + c + ''' * price_''' + c + '''
    sum_eur_after_fees = sum_eur - fee_limit_order_sell_''' + c + '''(sum_eur)
    sum_''' + c + '''_after_fees = sum_eur_after_fees / price_''' + c + '''
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(''' + c + '''=F("''' + c + '''") - sum_''' + c + ''')
        if bal[0].btc < 0: raise ValueError
        Order_sell_''' + c + '''.objects.create(
            user=user,
            ''' + c + '''=sum_''' + c + '''_after_fees,
            price=price_''' + c + ''',
            datetime=timezone.now()
        )

def delete_limit_order_sell_''' + c + '''(order_id):
    order = Order_sell_''' + c + '''.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    with transaction.atomic():
        order.delete()
        bal.update(''' + c + '''=F("''' + c + '''") + order.''' + c + ''')

''')


