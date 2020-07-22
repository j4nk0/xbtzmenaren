from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from . import rates
from .models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.db import transaction
from django.db.models import F, Sum
from decimal import Decimal as D
from decimal import InvalidOperation
from schwifty import IBAN
from .check_address import is_valid_btc_address, is_valid_ltc_address
import json

def dec(n, decimal_places):
    try:
        decimal = D(n)
    except InvalidOperation:
        raise ValueError
    rounded = decimal.quantize(D('0.1') ** decimal_places)
    if rounded != decimal:
        raise ValueError
    if decimal <= 0:
        raise ValueError
    return decimal

@login_required
def buy(request, success=None, active='btc'):
    sum_eur = request.user.balance.eur
    context = {
        'max_sum_eur': sum_eur,
        'active': active,
        'fee_btc': rates.fee_market_buy_btc(sum_eur),
        'sum_btc': rates.preview_market_buy_btc(sum_eur),
        'fee_ltc': rates.fee_market_buy_ltc(sum_eur),
        'sum_ltc': rates.preview_market_buy_ltc(sum_eur),
    }
    if success == True:
        context.update({'ok_message': "Nákup uspešný"})
    if success == False:
        context.update({'error_message': "Nesprávna hodnota"})
    return render(request, 'xbtzmenarenapp/buy.html', context)

@login_required
def buy_btc(request):
    try:
        sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    except ValueError:
        return buy(request, False, 'btc')
    sum_btc = sum_eur / rates.get_btceur_buy()
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(eur=F('eur') - sum_eur)
            balance.update(btc=F('btc') + sum_btc)
            Buy_btc.objects.create(user=request.user, datetime=timezone.now(), btc=sum_btc, eur=sum_eur)
            if balance[0].eur < 0: raise ValueError
    except ValueError:
        return buy(request, False, 'btc')
    return buy(request, True, 'btc')

def buy_btc_json(request):
    sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    data = {
        'fee': str(rates.fee_market_buy_btc(sum_eur)),
        'btc': str(rates.preview_market_buy_btc(sum_eur)),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@login_required
def buy_ltc(request):
    try:
        sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    except ValueError:
        return buy(request, False, 'ltc')
    sum_ltc = sum_eur / rates.get_ltceur_buy()
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(eur=F('eur') - sum_eur)
            balance.update(ltc=F('ltc') + sum_ltc)
            Buy_ltc.objects.create(user=request.user, datetime=timezone.now(), ltc=sum_ltc, eur=sum_eur)
            if balance[0].eur < 0: raise ValueError
    except ValueError:
        return buy(request, False, 'ltc')
    return buy(request, True, 'ltc')

def buy_ltc_json(request):
    sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    data = {
        'fee': str(rates.fee_market_buy_ltc(sum_eur)),
        'ltc': str(rates.preview_market_buy_ltc(sum_eur)),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@login_required
def sell(request, success=None, active='btc'):
    sum_btc = request.user.balance.btc
    sum_ltc = request.user.balance.ltc
    fee_btc, sum_eur_btc = rates.preview_market_sell_btc(sum_btc)
    fee_ltc, sum_eur_ltc = rates.preview_market_sell_ltc(sum_ltc)
    context = {
        'max_sum_btc': sum_btc,
        'max_sum_ltc': sum_ltc,
        'active': active,
        'fee_btc': fee_btc,
        'sum_eur_btc': sum_eur_btc,
        'fee_ltc': fee_ltc,
        'sum_eur_ltc': sum_eur_ltc,
    }
    if success == True:
        context.update({'ok_message': "Predaj uspešný"})
    if success == False:
        context.update({'error_message': "Nesprávna hodnota"})
    return render(request, 'xbtzmenarenapp/sell.html', context)

@login_required
def sell_btc(request):
    try:
        sum_btc = dec(request.POST['sum_btc'], DECIMAL_PLACES_BTC)
    except ValueError:
        return sell(request, False, 'btc')
    sum_eur = sum_btc * rates.get_btceur_sell()
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(eur=F('eur') + sum_eur)
            balance.update(btc=F('btc') - sum_btc)
            Sell_btc.objects.create(user=request.user, datetime=timezone.now(), btc=sum_btc, eur=sum_eur)
            if balance[0].btc < 0: raise ValueError
    except ValueError:
        return sell(request, False, 'btc')
    return sell(request, True, 'btc')

def sell_btc_json(request):
    sum_btc = dec(request.POST['sum_btc'], DECIMAL_PLACES_BTC)
    fee, sum_eur = rates.preview_market_sell_btc(sum_btc)
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@login_required
def sell_ltc(request):
    try:
        sum_ltc = dec(request.POST['sum_ltc'], DECIMAL_PLACES_LTC)
    except ValueError:
        return sell(request, False, 'ltc')
    sum_eur = sum_ltc * rates.get_ltceur_sell()
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(eur=F('eur') + sum_eur)
            balance.update(ltc=F('ltc') - sum_ltc)
            Sell_ltc.objects.create(user=request.user, datetime=timezone.now(), ltc=sum_ltc, eur=sum_eur)
            if balance[0].ltc < 0: raise ValueError
    except ValueError:
        sell(request, False, 'ltc')
    return sell(request, True, 'ltc')

def sell_ltc_json(request):
    sum_ltc = dec(request.POST['sum_ltc'], DECIMAL_PLACES_LTC)
    fee, sum_eur = rates.preview_market_sell_ltc(sum_ltc)
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@login_required
def private_rates(request):
    context = {
        'btceur_buy': rates.rates()['BTC-EUR']['buy'],
        'btceur_sell': rates.rates()['BTC-EUR']['sell'],
        'ltceur_buy': rates.rates()['LTC-EUR']['buy'],
        'ltceur_sell': rates.rates()['LTC-EUR']['sell'],
    }
    return render(request, 'xbtzmenarenapp/privateRates.html', context)

def public_rates(request):
    context = {
        'btceur_buy': rates.rates()['BTC-EUR']['buy'],
        'btceur_sell': rates.rates()['BTC-EUR']['sell'],
        'ltceur_buy': rates.rates()['LTC-EUR']['buy'],
        'ltceur_sell': rates.rates()['LTC-EUR']['sell'],
    }
    return render(request, 'xbtzmenarenapp/publicRates.html', context)

def rates_json(request):
    res = HttpResponse(jsom.dumps(rates.rates()))
    res['Content-Type'] = 'application/json'
    return res

def terms_and_conditions(request):
    return render(request, 'xbtzmenarenapp/terms.html', {})

def contacts(request):
    return render(request, 'xbtzmenarenapp/contacts.html', {})

def registration(request, error_message=None):
    context = { 'error_message': error_message }
    return render(request, 'xbtzmenarenapp/registration.html', context)
        
def registration_attempt(request):
    if request.POST['password'] != request.POST['password-again']:
        return registration(request, 'Heslá sa nezhodujú')
    email = request.POST['email']
    try:
        validate_email(email)
    except ValidationError:
        return registration(request, 'Neplatný e-mail')
    password = request.POST['password']
    try:
        validate_password(password, request.user)
    except ValidationError:
        return registration(request, 'Slabé heslo')
    try:
        CustomUser.objects.create_user(email, password=password)
    except:
        return registration(request, 'Email je už registrovaný')
    Address.objects.create(
        user=CustomUser.objects.get(email=email),
        vs=f'{CustomUser.objects.get(email=email).id:010}',
        btc='BTC_address:' + email[:88],
        ltc='LTC_address:' + email[:88],
    )
    Balance.objects.create(
        user=CustomUser.objects.get(email=email),
        eur=0,
        btc=0,
        ltc=0,
    )
    return redirect('login')

@login_required
def portfolio(request):
    context = {
        'eur': request.user.balance.eur,
        'btc': request.user.balance.btc,
        'ltc': request.user.balance.ltc,
    }
    return render(request, 'xbtzmenarenapp/portfolio.html', context)

@login_required
def change_password(request, error_message=None):
    context = { 'error_message': error_message }
    return render(request, 'xbtzmenarenapp/changePassword.html', context)

@login_required
def change_password_attempt(request):
    if request.POST['password'] != request.POST['password-again']:
        return change_password(request, 'Heslá sa nezhodujú')
    password = request.POST['password'] 
    try:
        validate_password(password, request.user)
    except ValidationError:
        return change_password(request, 'Slabé heslo')
    user = CustomUser.objects.get(email=request.user.email)
    user.set_password(password)
    user.save()
    return redirect('logout')

@login_required
def deposit(request):
    context = { 
        'vs': request.user.address.vs, 
        'btc_address': request.user.address.btc, 
        'ltc_address': request.user.address.ltc,
    }
    return render(request, 'xbtzmenarenapp/deposit.html', context)

@login_required
def withdrawal(request, error_message=None, ok_message=None, active='eur'):
    context = {
        'error_message': error_message,
        'ok_message': ok_message,
        'max_sum_eur': request.user.balance.eur,
        'max_sum_btc': request.user.balance.btc,
        'max_sum_ltc': request.user.balance.ltc,
        'fee_btc': 0.0001,
        'fee_ltc': 0.0005,
        'active': active,
    }
    return render(request, 'xbtzmenarenapp/withdrawal.html', context)

@login_required
def withdrawal_eur(request):
    try:
        sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='eur')
    iban = request.POST['account_number']
    try:
        iban = IBAN(iban).formatted
    except ValueError:
        return withdrawal(request, error_message='Nesprávny IBAN', active='eur')
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(eur=F('eur') - sum_eur)
            Withdrawal_eur.objects.create(
                user=request.user,
                time_created=timezone.now(),
                eur=sum_eur,
                is_pending=True,
                iban=iban,
            )
            if balance[0].eur < 0: raise ValueError
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='eur')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='eur')

@login_required
def withdrawal_btc(request):
    try:
        sum_btc = dec(request.POST['sum_btc'], DECIMAL_PLACES_BTC)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='btc')
    address_btc = request.POST['address_btc']
    if not is_valid_btc_address(address_btc):
        return withdrawal(request, error_message='Nesprávna adresa', active='btc')
    is_instant = True if 'is_instant_btc' in request.POST else False
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(btc=F('btc') - sum_btc)
            if is_instant:
                Withdrawal_btc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    time_processed=timezone.now(),
                    btc=sum_btc,
                    address=address_btc,
                    is_pending=False,
                )
                # do smtg
            else:
                Withdrawal_btc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    btc=sum_btc,
                    address=address_btc,
                    is_pending=True,
                )
            if balance[0].btc < 0: raise ValueError
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='btc')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='btc')

@login_required
def withdrawal_ltc(request):
    try:
        sum_ltc = dec(request.POST['sum_ltc'], DECIMAL_PLACES_LTC)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='ltc')
    address_ltc = request.POST['address_ltc']
    if not is_valid_ltc_address(address_ltc):
        return withdrawal(request, error_message='Nesprávna adresa', active='ltc')
    is_instant = True if 'is_instant_ltc' in request.POST else False
    try:
        with transaction.atomic():
            balance = Balance.objects.filter(user=request.user)
            balance.update(ltc=F('ltc') - sum_ltc)
            if is_instant:
                Withdrawal_ltc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    time_processed=timezone.now(),
                    ltc=sum_ltc,
                    address=address_ltc,
                    is_pending=False,
                )
                # do smtg
            else:
                Withdrawal_ltc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    ltc=sum_ltc,
                    address=address_ltc,
                    is_pending=True,
                )
            if balance[0].ltc < 0: raise ValueError
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='ltc')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='ltc')


def staff_check(user):
    return user.is_staff

@user_passes_test(staff_check)
@login_required
def management_verification(request, success=None):
    context = {}
    if success == True:
        context.update({'ok_message': "Užívateľ overený"})
    if success == False:
        context.update({'error_message': "Užívateľ nenájdený"})
    return render(request, 'xbtzmenarenapp/management/verification.html', context)

@user_passes_test(staff_check)
@login_required
def management_verification_attempt(request):
    email = request.POST['email']
    try:
        user = CustomUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return management_verification(request, False)
    user.is_verified = True
    user.save()
    return management_verification(request, True)

@user_passes_test(staff_check)
@login_required
def management_withdrawals(request, active='eur'):
    context = {
        'old_withdrawals_eur': Withdrawal_eur.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'old_withdrawals_btc': Withdrawal_btc.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'old_withdrawals_ltc': Withdrawal_ltc.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'withdrawals_eur': Withdrawal_eur.objects.filter(is_pending=True).order_by('iban')[:100],
        'withdrawals_btc': Withdrawal_btc.objects.filter(is_pending=True).order_by('address')[:100],
        'withdrawals_ltc': Withdrawal_ltc.objects.filter(is_pending=True).order_by('address')[:100],
        'active': active,
    }
    return render(request, 'xbtzmenarenapp/management/withdrawals.html', context)

@user_passes_test(staff_check)
@login_required
def management_withdrawal_eur_check(request, withdrawal_id):
    withdrawal = Withdrawal_eur.objects.get(id=withdrawal_id)
    withdrawal.is_pending = False
    withdrawal.time_processed=timezone.now()
    withdrawal.save()
    return management_withdrawals(request, 'eur')

@user_passes_test(staff_check)
@login_required
def management_withdrawal_btc_check(request, withdrawal_id):
    withdrawal = Withdrawal_btc.objects.get(id=withdrawal_id)
    withdrawal.is_pending = False
    withdrawal.time_processed=timezone.now()
    withdrawal.save()
    return management_withdrawals(request, 'btc')

@user_passes_test(staff_check)
@login_required 
def management_withdrawal_ltc_check(request, withdrawal_id):
    withdrawal = Withdrawal_ltc.objects.get(id=withdrawal_id)
    withdrawal.is_pending = False
    withdrawal.time_processed=timezone.now()
    withdrawal.save()
    return management_withdrawals(request, 'ltc')

@user_passes_test(staff_check)
@login_required
def management_deposits(request, error_message=None):
    context = {
        'deposits_eur': Deposit_eur.objects.all().order_by('-datetime')[:10],
        'error_message': error_message,
    }
    return render(request, 'xbtzmenarenapp/management/deposits.html', context)


@user_passes_test(staff_check)
@login_required
def management_deposit_attempt(request):
    vs = request.POST['vs']
    try:
        sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    except ValueError:
        return management_deposits(request, 'Neplatná hodnota')
    try:
        with transaction.atomic():
            address = Address.objects.get(vs=vs)
            user = address.user
            balance = user.balance
            Deposit_eur.objects.create(user=user, vs=vs, eur=sum_eur, datetime=timezone.now())
            balance.eur += sum_eur
            balance.save()
    except ObjectDoesNotExist:
        return management_deposits(request, 'Neplatný variabilný symbol')
    return management_deposits(request)

@user_passes_test(staff_check)
@login_required
def management_balances(request):
    total_eur = Balance.objects.aggregate(Sum('eur'))['eur__sum']
    total_btc = Balance.objects.aggregate(Sum('btc'))['btc__sum']
    total_ltc = Balance.objects.aggregate(Sum('ltc'))['ltc__sum']
    staff_eur = 0
    staff_btc = 0
    staff_ltc = 0
    staff_users = CustomUser.objects.filter(is_staff=True)
    for user in staff_users:
        staff_eur += user.balance.eur
        staff_btc += user.balance.btc
        staff_ltc += user.balance.ltc
    non_staff_eur = total_eur - staff_eur
    non_staff_btc = total_btc - staff_btc
    non_staff_ltc = total_ltc - staff_ltc
    context = {
        'non_staff_eur': non_staff_eur,
        'staff_eur': staff_eur,
        'total_eur': total_eur,
        'non_staff_btc': non_staff_btc,
        'staff_btc': staff_btc,
        'total_btc': total_btc,
        'non_staff_ltc': non_staff_ltc,
        'staff_ltc': staff_ltc,
        'total_ltc': total_ltc,
    }
    return render(request, 'xbtzmenarenapp/management/balances.html', context)

@user_passes_test(staff_check)
@login_required
def management_buys(request):
    context = {
        'buys_btc': Buy_btc.objects.all().order_by('-datetime')[:100],
        'buys_ltc': Buy_ltc.objects.all().order_by('-datetime')[:100],
    }
    return render(request, 'xbtzmenarenapp/management/buys.html', context)

@user_passes_test(staff_check)
@login_required
def management_sells(request):
    context = {
        'sells_btc': Sell_btc.objects.all().order_by('-datetime')[:100],
        'sells_ltc': Sell_ltc.objects.all().order_by('-datetime')[:100],
    }
    return render(request, 'xbtzmenarenapp/management/sells.html', context)
