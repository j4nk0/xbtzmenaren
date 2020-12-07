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

def fee_market_buy_doge(sum_eur):
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

def preview_market_buy_doge(sum_eur):
    sum_eur = D(sum_eur) - fee_market_buy_doge(sum_eur)
    sum_doge = 0
    for order in Order_sell_doge.objects.all().order_by('price'):
        if order.doge * order.price > sum_eur:
           sum_doge += sum_eur / order.price
           break
        else:
            sum_eur -= order.doge * order.price
            sum_doge += order.doge
    if sum_doge <= 0: return 0
    return r(sum_doge.quantize(D(0.1) ** DECIMAL_PLACES_DOGE))

def market_buy_btc(user, sum_eur):
    sum_eur_before_fees = D(sum_eur)
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(eur=F('eur') - D(sum_eur))
        if bal.eur < 0: raise ValueError('Not enough funds')
        Order_sell_btc.objects.all().select_for_update()
        sum_eur = D(sum_eur) - fee_market_buy_btc(sum_eur)
        sum_btc = 0
        for order in Order_sell_btc.objects.all().order_by('price'):
            if order.btc * order.price >= sum_eur:
                sum_btc += sum_eur / order.price
                order.btc -= sum_eur / order.price 
                order.save()
                if order.btc == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + sum_eur)
                break
            else:
                sum_eur -= order.btc * order.price
                sum_btc += order.btc
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + order.btc * order.price)
        else:
            raise ValueError('Market order too big, not enough sell orders to accomodate')
        bal.update(btc=F('btc') + D(sum_btc))
        Buy_btc.objects.create(
            user=user,
            datetime=timezone.now(),
            btc=sum_btc,
            eur=sum_eur_before_fees,
        )

def market_buy_ltc(user, sum_eur):
    sum_eur_before_fees = D(sum_eur)
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(eur=F('eur') - D(sum_eur))
        if bal.eur < 0: raise ValueError('Not enough funds')
        Order_sell_ltc.objects.all().select_for_update()
        sum_eur = D(sum_eur) - fee_market_buy_ltc(sum_eur)
        sum_ltc = 0
        for order in Order_sell_ltc.objects.all().order_by('price'):
            if order.ltc * order.price >= sum_eur:
                sum_ltc += sum_eur / order.price
                order.ltc -= sum_eur / order.price 
                order.save()
                if order.ltc == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + sum_eur)
                break
            else:
                sum_eur -= order.ltc * order.price
                sum_ltc += order.ltc
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + order.ltc * order.price)
        else:
            raise ValueError('Market order too big, not enough sell orders to accomodate')
        bal.update(ltc=F('ltc') + D(sum_ltc))
        Buy_ltc.objects.create(
            user=user,
            datetime=timezone.now(),
            ltc=sum_ltc,
            eur=sum_eur_before_fees,
        )

def market_buy_doge(user, sum_eur):
    sum_eur_before_fees = D(sum_eur)
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(eur=F('eur') - D(sum_eur))
        if bal.eur < 0: raise ValueError('Not enough funds')
        Order_sell_doge.objects.all().select_for_update()
        sum_eur = D(sum_eur) - fee_market_buy_doge(sum_eur)
        sum_doge = 0
        for order in Order_sell_doge.objects.all().order_by('price'):
            if order.doge * order.price >= sum_eur:
                sum_doge += sum_eur / order.price
                order.doge -= sum_eur / order.price 
                order.save()
                if order.doge == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + sum_eur)
                break
            else:
                sum_eur -= order.doge * order.price
                sum_ltc += order.doge
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + order.doge * order.price)
        else:
            raise ValueError('Market order too big, not enough sell orders to accomodate')
        bal.update(ltc=F('doge') + D(sum_doge))
        Buy_doge.objects.create(
            user=user,
            datetime=timezone.now(),
            doge=sum_doge,
            eur=sum_eur_before_fees,
        )

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

def fee_market_sell_doge(sum_eur):
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

def preview_market_sell_doge(sum_doge):
    sum_doge = D(sum_doge)
    sum_eur = 0
    for order in Order_buy_doge.objects.all().order_by('-price'):
        if order.doge > sum_doge:
            sum_eur += sum_doge * order.price
            break
        else:
            sum_doge -= order.doge
            sum_eur += order.doge * order.price
    fee = r(fee_market_sell_doge(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return (fee, sum_eur)


def market_sell_btc(user, sum_btc):
    sum_btc = D(sum_btc)
    original_sum_btc = sum_btc
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(btc=F('btc') - sum_btc)
        if bal.btc < 0: raise ValueError('Not enough funds')
        Order_buy_btc.objects.all().select_for_update()
        sum_eur = 0
        for order in Order_buy_btc.objects.all().order_by('-price'):
            if order.btc >= sum_btc:
                sum_eur += sum_btc * order.price
                order.btc -= sum_btc
                order.save()
                if order.btc == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(btc=F('btc') + sum_btc)
                break
            else:
                sum_btc -= order.btc
                sum_eur += order.btc * order.price
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(btc=F('btc') + order.btc)
        else:
            raise ValueError('Market order too big, not enough buy orders to accomodate')
        sum_eur -= fee_market_sell_btc(sum_eur)
        bal.update(eur=F('eur') + sum_eur)
        Sell_btc.objects.create(
            user=user,
            datetime=timezone.now(),
            btc=original_sum_btc,
            eur=sum_eur,
        )

def market_sell_ltc(user, sum_ltc):
    sum_ltc = D(sum_ltc)
    original_sum_ltc = sum_ltc
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(ltc=F('ltc') - sum_ltc)
        if bal.ltc < 0: raise ValueError('Not enough funds')
        Order_buy_ltc.objects.all().select_for_update()
        sum_eur = 0
        for order in Order_buy_ltc.objects.all().order_by('-price'):
            if order.ltc >= sum_ltc:
                sum_eur += sum_ltc * order.price
                order.ltc -= sum_ltc
                order.save()
                if order.ltc == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(ltc=F('ltc') + sum_ltc)
                break
            else:
                sum_ltc -= order.ltc
                sum_eur += order.ltc * order.price
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(ltc=F('ltc') + order.ltc)
        else:
            raise ValueError('Market order too big, not enough buy orders to accomodate')
        sum_eur -= fee_market_sell_ltc(sum_eur)
        bal.update(eur=F('eur') + sum_eur)
        Sell_ltc.objects.create(
            user=user,
            datetime=timezone.now(),
            ltc=original_sum_ltc,
            eur=sum_eur,
        )

def market_sell_doge(user, sum_doge):
    sum_doge = D(sum_doge)
    original_sum_doge = sum_doge
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(doge=F('doge') - sum_doge)
        if bal.doge < 0: raise ValueError('Not enough funds')
        Order_buy_doge.objects.all().select_for_update()
        sum_eur = 0
        for order in Order_buy_doge.objects.all().order_by('-price'):
            if order.doge >= sum_doge:
                sum_eur += sum_doge * order.price
                order.doge -= sum_doge
                order.save()
                if order.doge == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(doge=F('doge') + sum_doge)
                break
            else:
                sum_doge -= order.doge
                sum_eur += order.doge * order.price
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(doge=F('doge') + order.doge)
        else:
            raise ValueError('Market order too big, not enough buy orders to accomodate')
        sum_eur -= fee_market_sell_doge(sum_eur)
        bal.update(eur=F('eur') + sum_eur)
        Sell_doge.objects.create(
            user=user,
            datetime=timezone.now(),
            doge=original_sum_doge,
            eur=sum_eur,
        )

#=======================LIMIT ORDER BUYS============================================================

def fee_limit_order_buy_btc(sum_eur):
    return D(0)

def fee_limit_order_buy_ltc(sum_eur):
    return D(0)

def fee_limit_order_buy_doge(sum_eur):
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

def preview_limit_order_buy_doge(sum_doge, price_doge):
    sum_eur = sum_doge * price_doge
    fee = r(fee_limit_order_buy_doge(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_buy_btc(user, sum_btc, price_btc):
    try:
        if price_btc >= Order_sell_btc.objects.all().order_by('price')[0].price: raise ValueError
    except IndexError:
        pass
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
    try:
        if price_ltc >= Order_sell_ltc.objects.all().order_by('price')[0].price: raise ValueError
    except IndexError:
        pass
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

def limit_order_buy_doge(user, sum_doge, price_doge):
    try:
        if price_doge >= Order_sell_doge.objects.all().order_by('price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_doge * price_doge
    sum_eur_after_fees = sum_eur - fee_limit_order_buy_doge(sum_eur)
    sum_doge_after_fees = sum_eur_after_fees / price_doge
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(eur=F('eur') - sum_eur)
        if bal[0].eur < 0: raise ValueError
        Order_buy_doge.objects.create(
            user=user,
            doge=sum_doge_after_fees,
            price=price_doge,
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

def delete_limit_order_buy_doge(order_id):
    order = Order_buy_doge.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    sum_eur = order.doge * order.price
    with transaction.atomic():
        order.delete()
        bal.update(eur=F('eur') + sum_eur)

#=======================LIMIT ORDER SELLS===========================================================

def fee_limit_order_sell_btc(sum_eur):
    return D(0)

def fee_limit_order_sell_ltc(sum_eur):
    return D(0)

def fee_limit_order_sell_doge(sum_eur):
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

def preview_limit_order_sell_doge(sum_doge, price_doge):
    sum_eur = sum_doge * price_doge
    fee = r(fee_limit_order_sell_doge(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_sell_btc(user, sum_btc, price_btc):
    try:
        if price_btc <= Order_buy_btc.objects.all().order_by('-price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_btc * price_btc
    sum_eur_after_fees = sum_eur - fee_limit_order_sell_btc(sum_eur)
    sum_btc_after_fees = sum_eur_after_fees / price_btc
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(btc=F('btc') - sum_btc)
        if bal[0].btc < 0: raise ValueError
        Order_sell_btc.objects.create(
            user=user,
            btc=sum_btc_after_fees,
            price=price_btc,
            datetime=timezone.now()
        )

def limit_order_sell_ltc(user, sum_ltc, price_ltc):
    try:
        if price_ltc <= Order_buy_ltc.objects.all().order_by('-price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_ltc * price_ltc
    sum_eur_after_fees = sum_eur - fee_limit_order_sell_ltc(sum_eur)
    sum_ltc_after_fees = sum_eur_after_fees / price_ltc
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(ltc=F('ltc') - sum_ltc)
        if bal[0].ltc < 0: raise ValueError
        Order_sell_ltc.objects.create(
            user=user,
            ltc=sum_ltc_after_fees,
            price=price_ltc,
            datetime=timezone.now()
        )

def limit_order_sell_doge(user, sum_doge, price_doge):
    try:
        if price_doge <= Order_buy_doge.objects.all().order_by('-price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_doge * price_doge
    sum_eur_after_fees = sum_eur - fee_limit_order_sell_doge(sum_eur)
    sum_doge_after_fees = sum_eur_after_fees / price_doge
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(doge=F('doge') - sum_doge)
        if bal[0].ltc < 0: raise ValueError
        Order_sell_ltc.objects.create(
            user=user,
            doge=sum_doge_after_fees,
            price=price_doge,
            datetime=timezone.now()
        )

def delete_limit_order_sell_btc(order_id):
    order = Order_sell_btc.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    with transaction.atomic():
        order.delete()
        bal.update(btc=F('btc') + order.btc)

def delete_limit_order_sell_ltc(order_id):
    order = Order_sell_ltc.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    with transaction.atomic():
        order.delete()
        bal.update(ltc=F('ltc') + order.ltc)

def delete_limit_order_sell_doge(order_id):
    order = Order_sell_doge.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    with transaction.atomic():
        order.delete()
        bal.update(doge=F('doge') + order.doge)

