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
from .check_address import is_valid_btc_address, is_valid_ltc_address, is_valid_doge_address
import json
from . import bitcoin_driver
from . import litecoin_driver
from . import dogecoin_driver
from django import forms

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

def verification_check(user):
    return user.is_verified

@user_passes_test(verification_check)
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
        'fee_doge': rates.fee_market_buy_doge(sum_eur),
        'sum_doge': rates.preview_market_buy_doge(sum_eur),
    }
    if success == True:
        context.update({'ok_message': 'Nákup uspešný'})
    if success == False:
        context.update({'error_message': 'Nesprávna hodnota'})
    return render(request, 'xbtzmenarenapp/buy.html', context)

for c in CURRENCIES:
    exec('''
@user_passes_test(verification_check)
@login_required
def buy_''' + c + '''(request):
    try:
        sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
        rates.market_buy_''' + c + '''(request.user, sum_eur)
    except:
        return buy(request, False, "''' + c + '''")
    return buy(request, True, "''' + c + '''")

def buy_''' + c + '''_json(request):
    sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    data = {
        'fee': str(rates.fee_market_buy_''' + c + '''(sum_eur)),
        "''' + c + '''": str(rates.preview_market_buy_''' + c + '''(sum_eur)),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res
''')

@user_passes_test(verification_check)
@login_required
def sell(request, success=None, active='btc'):
    sum_btc = request.user.balance.btc
    sum_ltc = request.user.balance.ltc
    sum_doge = request.user.balance.doge
    fee_btc, sum_eur_btc = rates.preview_market_sell_btc(sum_btc)
    fee_ltc, sum_eur_ltc = rates.preview_market_sell_ltc(sum_ltc)
    fee_doge, sum_eur_doge = rates.preview_market_sell_doge(sum_doge)
    context = {
        'max_sum_btc': sum_btc,
        'max_sum_ltc': sum_ltc,
        'max_sum_doge': sum_doge,
        'active': active,
        'fee_btc': fee_btc,
        'sum_eur_btc': sum_eur_btc,
        'fee_ltc': fee_ltc,
        'sum_eur_ltc': sum_eur_ltc,
        'fee_doge': fee_doge,
        'sum_eur_doge': sum_eur_doge,
    }
    if success == True:
        context.update({'ok_message': 'Predaj uspešný'})
    if success == False:
        context.update({'error_message': 'Nesprávna hodnota'})
    return render(request, 'xbtzmenarenapp/sell.html', context)

for c in CURRENCIES:
    exec('''
@user_passes_test(verification_check)
@login_required
def sell_''' + c + '''(request):
    try:
        sum_''' + c + ''' = dec(request.POST['sum_''' + c + ''''], ''' + DECIMAL_PLACES[c] + ''')
        rates.market_sell_''' + c + '''(request.user, sum_''' + c + ''')
    except:
        return sell(request, False, "''' + c + '''")
    return sell(request, True, "''' + c + '''")

def sell_''' + c + '''_json(request):
    sum_''' + c + ''' = dec(request.POST['sum_''' + c + ''''], ''' + DECIMAL_PLACES[c] + ''')
    fee, sum_eur = rates.preview_market_sell_''' + c + '''(sum_''' + c + ''')
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res
''')

@user_passes_test(verification_check)
@login_required
def limit_order_buy(request, success=None, active='btc'):
    context = {
        'active': active,
        'max_sum_eur': request.user.balance.eur,
        'orders_btc': Order_buy_btc.objects.filter(user=request.user),
        'orders_ltc': Order_buy_ltc.objects.filter(user=request.user),
        'orders_doge': Order_buy_doge.objects.filter(user=request.user),
    }
    if success == True:
        context.update({'ok_message': 'Požiadavka registrovaná'})
    if success == False:
        context.update({'error_message': 'Nesprávna hodnota'})
    return render(request, 'xbtzmenarenapp/limitOrderBuy.html', context)

for c in CURRENCIES:
    exec('''
@user_passes_test(verification_check)
@login_required
def limit_order_buy_''' + c + '''(request):
    try:
        sum_''' + c + ''' = dec(request.POST['sum_''' + c + ''''], ''' + DECIMAL_PLACES[c] + ''')
        price_''' + c + ''' = dec(request.POST['price_''' + c + ''''], DECIMAL_PLACES_PRICE)
        rates.limit_order_buy_''' + c + '''(request.user, sum_''' + c + ''', price_''' + c + ''')
    except:
        return limit_order_buy(request, False, "''' + c + '''")
    return limit_order_buy(request, True, "''' + c + '''")

def limit_order_buy_''' + c + '''_json(request):
    sum_''' + c + ''' = dec(request.POST['sum_''' + c + ''''], ''' + DECIMAL_PLACES[c] + ''')
    price_''' + c + ''' = dec(request.POST['price_''' + c + ''''], DECIMAL_PLACES_PRICE)
    fee, sum_eur = rates.preview_limit_order_buy_''' + c + '''(sum_''' + c + ''', price_''' + c + ''')
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@user_passes_test(verification_check)
@login_required
def limit_order_buy_''' + c + '''_delete(request, order_id):
    if request.user != Order_buy_''' + c + '''.objects.get(id=order_id).user:
        return limit_order_buy(request, False, "''' + c + '''")
    try:
        rates.delete_limit_order_buy_''' + c + '''(order_id)
    except:
        return limit_order_buy(request, False, "''' + c + '''")
    return limit_order_buy(request, True, "''' + c + '''btc")
''')

@user_passes_test(verification_check)
@login_required
def limit_order_sell(request, success=None, active='btc'):
    context = {
        'active': active,
        'max_sum_btc': request.user.balance.btc,
        'max_sum_ltc': request.user.balance.ltc,
        'max_sum_doge': request.user.balance.doge,
        'orders_btc': Order_sell_btc.objects.filter(user=request.user),
        'orders_ltc': Order_sell_ltc.objects.filter(user=request.user),
        'orders_doge': Order_sell_doge.objects.filter(user=request.user),
    }
    if success == True:
        context.update({'ok_message': 'Požiadavka registrovaná'})
    if success == False:
        context.update({'error_message': 'Nesprávna hodnota'})
    return render(request, 'xbtzmenarenapp/limitOrderSell.html', context)

for c in CURRENCIES:
    exec('''
@user_passes_test(verification_check)
@login_required
def limit_order_sell_''' + c + '''(request):
    try:
        sum_''' + c + ''' = dec(request.POST['sum_''' + c + ''''], ''' + DECIMAL_PLACES[c] + ''')
        price_''' + c + ''' = dec(request.POST['price_''' + c + ''''], DECIMAL_PLACES_PRICE)
        rates.limit_order_sell_''' + c + '''(request.user, sum_''' + c + ''', price_''' + c + ''')
    except:
        return limit_order_sell(request, False, "''' + c + '''")
    return limit_order_sell(request, True, "''' + c + '''")

def limit_order_sell_''' + c + '''_json(request):
    sum_''' + c + ''' = dec(request.POST['sum_''' + c + ''''], ''' +  DECIMAL_PLACES[c] + ''')
    price_''' + c + ''' = dec(request.POST['price_''' + c + ''''], DECIMAL_PLACES_PRICE)
    fee, sum_eur = rates.preview_limit_order_sell_''' + c + '''(sum_''' + c + ''', price_''' + c + ''')
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@user_passes_test(verification_check)
@login_required
def limit_order_sell_''' + c + '''_delete(request, order_id):
    if request.user != Order_sell_''' + c + '''.objects.get(id=order_id).user:
        return limit_order_buy(request, False, "''' + c + '''")
    try:
        rates.delete_limit_order_sell_''' + c + '''(order_id)
    except:
        return limit_order_sell(request, False, "''' + c + '''")
    return limit_order_sell(request, True, "''' + c + '''")
''')

@user_passes_test(verification_check)
@login_required
def private_rates(request):
    context = {
        'btceur_buy': rates.rates()['BTC-EUR']['buy'],
        'btceur_sell': rates.rates()['BTC-EUR']['sell'],
        'ltceur_buy': rates.rates()['LTC-EUR']['buy'],
        'ltceur_sell': rates.rates()['LTC-EUR']['sell'],
        'dogeeur_buy': rates.rates()['DOGE-EUR']['buy'],
        'dogeeur_sell': rates.rates()['DOGE-EUR']['sell'],
    }
    return render(request, 'xbtzmenarenapp/privateRates.html', context)

def public_rates(request):
    context = {
        'btceur_buy': rates.rates()['BTC-EUR']['buy'],
        'btceur_sell': rates.rates()['BTC-EUR']['sell'],
        'ltceur_buy': rates.rates()['LTC-EUR']['buy'],
        'ltceur_sell': rates.rates()['LTC-EUR']['sell'],
        'dogeeur_buy': rates.rates()['DOGE-EUR']['buy'],
        'dogeeur_sell': rates.rates()['DOGE-EUR']['sell'],
    }
    return render(request, 'xbtzmenarenapp/publicRates.html', context)

def rates_json(request):
    data = rates.rates()
    data['BTC-EUR']['buy'] = str(data['BTC-EUR']['buy'])
    data['BTC-EUR']['sell'] = str(data['BTC-EUR']['sell'])
    data['LTC-EUR']['buy'] = str(data['LTC-EUR']['buy'])
    data['LTC-EUR']['sell'] = str(data['LTC-EUR']['sell'])
    data['DOGE-EUR']['buy'] = str(data['DOGE-EUR']['buy'])
    data['DOGE-EUR']['sell'] = str(data['DOGE-EUR']['sell'])
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

def terms_and_conditions(request):
    return render(request, 'xbtzmenarenapp/terms.html', {})

def contacts(request):
    return render(request, 'xbtzmenarenapp/contacts.html', {})

class QuestionareForm(forms.Form):
    id_img_front = forms.ImageField(label='Foto Občianskeho Preukazu spredu')
    id_img_back = forms.ImageField(label='Foto Občianskeho Preukazu zozadu')
    face_img = forms.ImageField(label='Foto tváre')
    q1 = forms.ChoiceField(
        label='Koľko EUR mienite investovať jednorázovo?',
        widget=forms.RadioSelect,
        choices=(
            ('1', '< 100'),
            ('2', '100 - 500'),
            ('3', '500 - 1 000'),
            ('4', '> 1 000'),
        ) 
    )
    q2 = forms.ChoiceField(
        label='Koľko EUR mienite investovať pravidelne mesačne?',
        widget=forms.RadioSelect,
        choices=(
            ('1', '< 100'),
            ('2', '100 - 500'),
            ('3', '500 - 1 000'),
            ('4', '> 1000'),
        ) 
    )
    q3 = forms.ChoiceField(
        label='Aká je priemerná výška vašich pravidelných ročných príjmov v EUR po zdanení? Uveďte prosím odhad vašeho priemerného ročného čistého príjmu. Jednorázové príjmy, vzniknuté napríklad predajom nehnuteľnosti, pozemkov, iných investícií a pod., nezapočítavajte.',
        widget=forms.RadioSelect,
        choices=(
            ('1', '< 4 000'),
            ('2', '4 000 - 20 000'),
            ('3', '20 000 - 40 000'),
            ('4', '> 40 000'),
        ) 
    )
    q4 = forms.ChoiceField(
        label='Na koľko EUR odhadujete hodnotu svojho majetku? Vrátane hotovosti, hnuteľných vecí, investícií a nehnuteľností. Skúste odhadnúť množstvo peňazí, ktoré by ste získali, ak by ste všetok svoj majetok naraz predali.',
        widget=forms.RadioSelect,
        choices=(
            ('1', '< 4 000'),
            ('2', '4 000 - 20 000'),
            ('3', '20 000 - 40 000'),
            ('4', '40 000 - 400 000'),
            ('5', '> 400 000'),
        ) 
    )
    q5 = forms.ChoiceField(
        label='Pravidelné splátky mojich súčasných finančných záväzkov (splátka hypotéky, leasingu, iného úveru a pod.) v percentách čistého príjmu dosahujú:',
        widget=forms.RadioSelect,
        choices=(
            ('1', '< 35 %'),
            ('2', '35 % - 50 %'),
            ('3', '> 50 %'),
        ) 
    )
    q6 = forms.ChoiceField(
        label='Čo je účelom vašich investícií?',
        widget=forms.RadioSelect,
        choices=(
            ('1', 'Primárne ochrániť svoje investované prostriedky.'),
            ('2', 'Mierne zhodnotiť svoje prostriedky a minimalizovať riziká.'),
            ('3', 'Zhodnotiť svoje prostriedky a znášať primerané riziko.'),
            ('4', 'Výrazne zhodnotiť svoje prostriedky aj za cenu veľmi vysokej kolísavosti hodnoty portfólia.'),
        ) 
    )
    q7 = forms.ChoiceField(
        label='Ako veľmi vám vadí krátkodobé a mnohokrát značné kolísanie hodnoty vášho portfólia oboma smermi?',
        widget=forms.RadioSelect,
        choices=(
            ('1', 'Vôbec mi nevadí.'),
            ('2', 'Skôr mi nevadí.'),
            ('3', 'Mám k tomu neutrálny postoj.'),
            ('4', 'Skôr mi vadí.'),
            ('5', 'Rozhodne mi vadí.'),
        ) 
    )
    q8 = forms.ChoiceField(
        label='Hodnota investície môže rásť aj klesať. O koľko by sa celková hodnota vašej investície musela znížiť, aby ste začali premýšľať o tom, že investíciu zrušíte?',
        widget=forms.RadioSelect,
        choices=(
            ('1', 'O 10 % a viac.'),
            ('2', 'O 20 % a viac.'),
            ('3', 'O 33 % a viac.'),
            ('4', 'O 50 % a viac.'),
            ('5', 'O rušení nepremýšľam, kým nevyprší plánovaný investičný horizont.'),
        ) 
    )
    q9 = forms.ChoiceField(
        label='Aká by bola vaša reakcia, ak by sa hodnota vášho portfólia prepadla o 10% v priebehu niekoľkých dní?',
        widget=forms.RadioSelect,
        choices=(
            ('1', 'Okamžite predám celé svoje portfólio a zabránim ďalším stratám.'),
            ('2', 'Predám časť svojho portfólia.'),
            ('3', 'Počkám na ďalší vývoj, kým sa hodnota nevráti.'),
            ('4', 'Využijem túto príležitosť a nakúpim viac za nižšie ceny.'),
        ) 
    )
    q10 = forms.ChoiceField(
        label='Ako by ovplyvnilo vašu životnú úroveň, ak by sa hodnota vašej investície významne znížila?',
        widget=forms.RadioSelect,
        choices=(
            ('1', 'Zásadne negatívne. Moja celková životná úroveň by sa znížila.'),
            ('2', 'Mierne. Moju životnú úroveň by to mohlo ohroziť.'),
            ('3', 'Neovplyvnilo. Dopad by bol zanedbateľný.'),
        ) 
    )
            
def registration(request, error_message=None):
    context = {
        'error_message': error_message,
        'questionare': QuestionareForm(),
    }
    return render(request, 'xbtzmenarenapp/registration.html', context)

def handle_uploaded_file(email, file_description, new_file):
    with open('media/' + email + file_description, 'wb+') as destination:
        for chunk in new_file.chunks():
            destination.write(chunk)

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
    try:
        handle_uploaded_file(email, '_id_img_front', request.FILES['id_img_front'])
        handle_uploaded_file(email, '_id_img_back', request.FILES['id_img_back'])
        handle_uploaded_file(email, '_face_img', request.FILES['face_img'])
        Address.objects.create(
            user=CustomUser.objects.get(email=email),
            vs=f'{CustomUser.objects.get(email=email).id:010}',
            btc=bitcoin_driver.get_new_address(),
            ltc=litecoin_driver.get_new_address(),
            doge=dogecoin_driver.get_new_address(),
        )
        Balance.objects.create(
            user=CustomUser.objects.get(email=email),
            eur=0,
            btc=0,
            ltc=0,
            doge=0,
        )
        Questionare.objects.create(
            user=CustomUser.objects.get(email=email),
            question1=int(request.POST['q1']),
            question2=int(request.POST['q2']),
            question3=int(request.POST['q3']),
            question4=int(request.POST['q4']),
            question5=int(request.POST['q5']),
            question6=int(request.POST['q6']),
            question7=int(request.POST['q7']),
            question8=int(request.POST['q8']),
            question9=int(request.POST['q9']),
            question10=int(request.POST['q10']),
        )
    except:
        raise
        CustomUser.objects.filter(email=email).delete()
        return registration(request, 'Chyba')
    return redirect('login')

@user_passes_test(verification_check)
@login_required
def portfolio(request):
    eur_in_orders = 0
    orders = Order_buy_btc.objects.filter(user=request.user)
    for o in orders: eur_in_orders += o.btc * o.price
    orders = Order_buy_ltc.objects.filter(user=request.user)
    for o in orders: eur_in_orders += o.ltc * o.price
    btc_in_orders = Order_sell_btc.objects.filter(user=request.user).aggregate(Sum('btc'))['btc__sum']
    if btc_in_orders == None: btc_in_orders = D(0)
    ltc_in_orders = Order_sell_ltc.objects.filter(user=request.user).aggregate(Sum('ltc'))['ltc__sum']
    if ltc_in_orders == None: ltc_in_orders = D(0)
    doge_in_orders = Order_sell_doge.objects.filter(user=request.user).aggregate(Sum('doge'))['doge__sum']
    if doge_in_orders == None: doge_in_orders = D(0)
    context = {
        'eur': rates.r(request.user.balance.eur),
        'btc': rates.r(request.user.balance.btc),
        'ltc': rates.r(request.user.balance.ltc),
        'doge': rates.r(request.user.balance.doge),
        'eur_in_orders': rates.r(eur_in_orders),
        'btc_in_orders': rates.r(btc_in_orders),
        'ltc_in_orders': rates.r(ltc_in_orders),
        'doge_in_orders': rates.r(doge_in_orders),
    }
    return render(request, 'xbtzmenarenapp/portfolio.html', context)

@user_passes_test(verification_check)
@login_required
def change_password(request, error_message=None):
    context = { 'error_message': error_message }
    return render(request, 'xbtzmenarenapp/changePassword.html', context)

@user_passes_test(verification_check)
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

@user_passes_test(verification_check)
@login_required
def deposit(request):
    context = { 
        'vs': request.user.address.vs, 
        'btc_address': request.user.address.btc, 
        'ltc_address': request.user.address.ltc,
        'doge_address': request.user.address.doge,
        'incoming_btc': Incoming_btc.objects.filter(user=request.user),
        'incoming_ltc': Incoming_ltc.objects.filter(user=request.user),
        'incoming_doge': Incoming_doge.objects.filter(user=request.user),
    }
    return render(request, 'xbtzmenarenapp/deposit.html', context)

@user_passes_test(verification_check)
@login_required
def withdrawal(request, error_message=None, ok_message=None, active='eur'):
    context = {
        'error_message': error_message,
        'ok_message': ok_message,
        'max_sum_eur': request.user.balance.eur,
        'max_sum_btc': request.user.balance.btc - bitcoin_driver.get_fee_per_kB(),
        'max_sum_ltc': request.user.balance.ltc - litecoin_driver.get_fee_per_kB(),
        'max_sum_doge': request.user.balance.doge + dogecoin_driver.get_fee_per_kB(),
        'active': active,
    }
    return render(request, 'xbtzmenarenapp/withdrawal.html', context)

@user_passes_test(verification_check)
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

@user_passes_test(verification_check)
@login_required
def withdrawal_btc(request):
    try:
        sum_btc = dec(request.POST['sum_btc'], DECIMAL_PLACES_BTC)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='btc')
    address_btc = request.POST['address_btc']
    if not is_valid_btc_address(address_btc):
        return withdrawal(request, error_message='Nesprávna adresa', active='btc')
    try:
        with transaction.atomic():
            fee = bitcoin_driver.get_fee_per_kB()
            balance = Balance.objects.filter(user=request.user)
            balance.update(btc=F('btc') - (sum_bt + fee))
            if balance[0].btc < 0: raise ValueError
            if bitcoin_driver.get_balance() < (sum_btc + fee):
                Withdrawal_btc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    btc=sum_btc,
                    address=address_btc,
                    is_pending=True,
                )
            else:
                Withdrawal_btc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    time_processed=timezone.now(),
                    btc=sum_btc,
                    address=address_btc,
                    is_pending=False,
                )
                bitcoin_driver.send(address_btc, sum_btc, fee)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='btc')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='btc')

@user_passes_test(verification_check)
@login_required
def withdrawal_ltc(request):
    try:
        sum_ltc = dec(request.POST['sum_ltc'], DECIMAL_PLACES_LTC)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='ltc')
    address_ltc = request.POST['address_ltc']
    if not is_valid_ltc_address(address_ltc):
        return withdrawal(request, error_message='Nesprávna adresa', active='ltc')
    try:
        with transaction.atomic():
            fee = litecoin_driver.get_fee_per_kB()
            balance = Balance.objects.filter(user=request.user)
            balance.update(ltc=F('ltc') - (sum_ltc + fee))
            if balance[0].ltc < 0: raise ValueError
            if litecoin_driver.get_balance() < (sum_ltc + fee):
                Withdrawal_ltc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    ltc=sum_ltc,
                    address=address_ltc,
                    is_pending=True,
                )
            else:
                Withdrawal_ltc.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    time_processed=timezone.now(),
                    ltc=sum_ltc,
                    address=address_ltc,
                    is_pending=False,
                )
                litecoin_driver.send(address_ltc, sum_ltc, fee)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='ltc')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='ltc')

@user_passes_test(verification_check)
@login_required
def withdrawal_doge(request):
    try:
        sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='doge')
    address_doge = request.POST['address_doge']
    if not is_valid_doge_address(address_doge):
        return withdrawal(request, error_message='Nesprávna adresa', active='doge')
    try:
        with transaction.atomic():
            fee = dogecoin_driver.get_fee_per_kB()
            balance = Balance.objects.filter(user=request.user)
            balance.update(doge=F('doge') - (sum_doge + fee))
            if balance[0].doge < 0: raise ValueError
            if dogecoin_driver.get_balance() < (sum_doge + fee):
                Withdrawal_doge.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    doge=sum_doge,
                    address=address_doge,
                    is_pending=True,
                )
            else:
                Withdrawal_doge.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    time_processed=timezone.now(),
                    doge=sum_doge,
                    address=address_doge,
                    is_pending=False,
                )
                dogecoin_driver.send(address_doge, sum_doge, fee)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='doge')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='doge')

def staff_check(user):
    return user.is_staff

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_verification(request, success=None):
    context = {
        'unverified': CustomUser.objects.filter(is_verified=False)
    }
    if success == True:
        context.update({'ok_message': "Užívateľ overený"})
    if success == False:
        context.update({'error_message': "Užívateľ nenájdený"})
    return render(request, 'xbtzmenarenapp/management/verification.html', context)

@user_passes_test(verification_check)
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

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_withdrawals(request, active='eur'):
    context = {
        'old_withdrawals_eur': Withdrawal_eur.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'old_withdrawals_btc': Withdrawal_btc.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'old_withdrawals_ltc': Withdrawal_ltc.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'old_withdrawals_doge': Withdrawal_doge.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        'withdrawals_eur': Withdrawal_eur.objects.filter(is_pending=True).order_by('iban')[:100],
        'withdrawals_btc': Withdrawal_btc.objects.filter(is_pending=True).order_by('address')[:100],
        'withdrawals_ltc': Withdrawal_ltc.objects.filter(is_pending=True).order_by('address')[:100],
        'withdrawals_doge': Withdrawal_doge.objects.filter(is_pending=True).order_by('address')[:100],
        'active': active,
    }
    return render(request, 'xbtzmenarenapp/management/withdrawals.html', context)

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_withdrawal_eur_check(request, withdrawal_id):
    withdrawal = Withdrawal_eur.objects.get(id=withdrawal_id)
    withdrawal.is_pending = False
    withdrawal.time_processed=timezone.now()
    withdrawal.save()
    return management_withdrawals(request, 'eur')

for c in CURRENCIES:
    exec('''
@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_withdrawal_''' + c + '''_check(request, withdrawal_id):
    withdrawal = Withdrawal_''' + c + '''.objects.get(id=withdrawal_id)
    withdrawal.is_pending = False
    withdrawal.time_processed=timezone.now()
    withdrawal.save()
    return management_withdrawals(request, "''' + c + '''")
''')

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_deposits(request, error_message=None):
    context = {
        'deposits_eur': Deposit_eur.objects.all().order_by('-datetime')[:10],
        'error_message': error_message,
    }
    return render(request, 'xbtzmenarenapp/management/deposits.html', context)


@user_passes_test(verification_check)
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

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_balances(request):
    eur_in_orders_staff = D(0)
    eur_in_orders_non_staff = D(0)
    orders = Order_buy_btc.objects.all()
    staff = CustomUser.objects.filter(is_staff=True)
    for o in orders:
        if o.user in staff:
            eur_in_orders_staff += o.btc * o.price
        else:
            eur_in_orders_non_staff += o.btc * o.price
    orders = Order_buy_ltc.objects.filter(user=request.user)
    for o in orders:
        if o.user in staff:
            eur_in_orders_staff += o.ltc * o.price
        else:
            eur_in_orders_non_staff += o.ltc * o.price
    orders = Order_buy_ltc.objects.filter(user=request.user)
    for o in orders:
        if o.user in staff:
            eur_in_orders_staff += o.doge * o.price
        else:
            eur_in_orders_non_staff += o.doge * o.price
    btc_in_orders_staff = D(0)
    btc_in_orders_non_staff = D(0)
    for user in CustomUser.objects.all():
        if user in staff:
            amount = Order_sell_btc.objects.filter(user=user).aggregate(Sum('btc'))['btc__sum']
            if amount: btc_in_orders_staff += amount
        else:
            amount = Order_sell_btc.objects.filter(user=user).aggregate(Sum('btc'))['btc__sum']
            if amount: btc_in_orders_non_staff += amount
    ltc_in_orders_staff = D(0)
    ltc_in_orders_non_staff = D(0)
    for user in CustomUser.objects.all():
        if user in staff:
            amount = Order_sell_ltc.objects.filter(user=user).aggregate(Sum('ltc'))['ltc__sum']
            if amount: ltc_in_orders_staff += amount
        else:
            amount = Order_sell_ltc.objects.filter(user=user).aggregate(Sum('ltc'))['ltc__sum']
            if amount: ltc_in_orders_non_staff += amount
    doge_in_orders_staff = D(0)
    doge_in_orders_non_staff = D(0)
    for user in CustomUser.objects.all():
        if user in staff:
            amount = Order_sell_doge.objects.filter(user=user).aggregate(Sum('doge'))['doge__sum']
            if amount: doge_in_orders_staff += amount
        else:
            amount = Order_sell_doge.objects.filter(user=user).aggregate(Sum('doge'))['doge__sum']
            if amount: doge_in_orders_non_staff += amount
    total_eur = Balance.objects.aggregate(Sum('eur'))['eur__sum']
    total_btc = Balance.objects.aggregate(Sum('btc'))['btc__sum']
    total_ltc = Balance.objects.aggregate(Sum('ltc'))['ltc__sum']
    total_doge = Balance.objects.aggregate(Sum('doge'))['doge__sum']
    staff_eur = D(0)
    staff_btc = D(0)
    staff_ltc = D(0)
    staff_doge = D(0)
    staff_users = CustomUser.objects.filter(is_staff=True)
    for user in staff_users:
        staff_eur += user.balance.eur
        staff_btc += user.balance.btc
        staff_ltc += user.balance.ltc
        staff_doge += user.balance.doge
    non_staff_eur = total_eur - staff_eur
    non_staff_btc = total_btc - staff_btc
    non_staff_ltc = total_ltc - staff_ltc
    non_staff_doge = total_doge - staff_doge
    context = {
        'eur_in_orders_staff': rates.r(eur_in_orders_staff),
        'eur_in_orders_non_staff': rates.r(eur_in_orders_non_staff),
        'eur_in_orders_total': rates.r(eur_in_orders_staff + eur_in_orders_non_staff),
        'btc_in_orders_staff': rates.r(btc_in_orders_staff),
        'btc_in_orders_non_staff': rates.r(btc_in_orders_non_staff),
        'btc_in_orders_total': rates.r(btc_in_orders_staff + btc_in_orders_non_staff),
        'ltc_in_orders_staff': rates.r(ltc_in_orders_staff),
        'ltc_in_orders_non_staff': rates.r(ltc_in_orders_non_staff),
        'ltc_in_orders_total': rates.r(ltc_in_orders_staff + ltc_in_orders_non_staff),
        'doge_in_orders_staff': rates.r(doge_in_orders_staff),
        'doge_in_orders_non_staff': rates.r(doge_in_orders_non_staff),
        'doge_in_orders_total': rates.r(doge_in_orders_staff + doge_in_orders_non_staff),
        'non_staff_eur': rates.r(non_staff_eur),
        'staff_eur': rates.r(staff_eur),
        'total_eur': rates.r(total_eur),
        'non_staff_btc': rates.r(non_staff_btc),
        'staff_btc': rates.r(staff_btc),
        'total_btc': rates.r(total_btc),
        'non_staff_ltc': rates.r(non_staff_ltc),
        'staff_ltc': rates.r(staff_ltc),
        'total_ltc': rates.r(total_ltc),
        'non_staff_doge': rates.r(non_staff_doge),
        'staff_doge': rates.r(staff_doge),
        'total_doge': rates.r(total_doge),
    }
    return render(request, 'xbtzmenarenapp/management/balances.html', context)

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_buys(request):
    context = {
        'buys_btc': Buy_btc.objects.all().order_by('-datetime')[:100],
        'buys_ltc': Buy_ltc.objects.all().order_by('-datetime')[:100],
        'buys_doge': Buy_doge.objects.all().order_by('-datetime')[:100],
    }
    return render(request, 'xbtzmenarenapp/management/buys.html', context)

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_sells(request):
    context = {
        'sells_btc': Sell_btc.objects.all().order_by('-datetime')[:100],
        'sells_ltc': Sell_ltc.objects.all().order_by('-datetime')[:100],
        'sells_doge': Sell_doge.objects.all().order_by('-datetime')[:100],
    }
    return render(request, 'xbtzmenarenapp/management/sells.html', context)

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required
def management_orderbook(request):
    context = {
        'buy_btc': Order_buy_btc.objects.all().order_by('-price')[:100:-1],
        'sell_btc': Order_sell_btc.objects.all().order_by('price')[:100],
        'buy_ltc': Order_buy_ltc.objects.all().order_by('-price')[:100:-1],
        'sell_ltc': Order_sell_ltc.objects.all().order_by('price')[:100],
        'buy_doge': Order_buy_doge.objects.all().order_by('-price')[:100:-1],
        'sell_doge': Order_sell_doge.objects.all().order_by('price')[:100],
    }
    return render(request, 'xbtzmenarenapp/management/orderbook.html', context)

@login_required
def wait_for_verification(request):
    return render(request, 'xbtzmenarenapp/waitForVerification.html', {})
