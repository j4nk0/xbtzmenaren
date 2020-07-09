from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from . import rates
from .models import CustomUser, Address, Balance
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
def index(request):
    return redirect('login')

@login_required
def buy(request, success=None):
    context = {
        'max_sum_eur': request.user.balance.eur,
    }
    if success == True:
        context.update({'ok_message': "Nákup uspešný"})
    if success == False:
        context.update({'error_message': "Nesprávna hodnota"})
    #template = loader.get_template('xbtzmenarenapp/buy.html')
    #return HttpResponse(template.render(context, request))
    return render(request, 'xbtzmenarenapp/buy.html', context)

@login_required
def buy_btc(request):
    sum_eur = request.POST['sum_eur']
    #return HttpResponse("coin: Bitcoin" + "\n"  + "sum: " + sum_eur)
    return buy(request, True)

@login_required
def buy_ltc(request):
    sum_eur = request.POST['sum_eur']
    return HttpResponse("coin: Litecoin" + "\n"  + "sum: " + sum_eur)

@login_required
def sell(request, success=None):
    context = {
        'max_sum_btc': request.user.balance.btc,
        'max_sum_ltc': request.user.balance.ltc,
    }
    if success == True:
        context.update({'ok_message': "Predaj uspešný"})
    if success == False:
        context.update({'error_message': "Nesprávna hodnota"})
    return render(request, 'xbtzmenarenapp/sell.html', context)

@login_required
def sell_btc(request):
    sum_btc = request.POST['sum_btc']
    return HttpResponse("coin: Bitcoin" + "\n"  + "sum: " + sum_btc)

@login_required
def sell_ltc(request):
    sum_ltc = request.POST['sum_ltc']
    return HttpResponse("coin: Litecoin" + "\n"  + "sum: " + sum_ltc)

@login_required
def private_rates(request):
    context = {
            'btceur_buy': rates.get_btceur_buy(),
            'btceur_sell': rates.get_btceur_sell(),
            'ltceur_buy': rates.get_ltceur_buy(),
            'ltceur_sell': rates.get_ltceur_sell(),
    }
    return render(request, 'xbtzmenarenapp/privateRates.html', context)

def public_rates(request):
    context = {
            'btceur_buy': rates.get_btceur_buy(),
            'btceur_sell': rates.get_btceur_sell(),
            'ltceur_buy': rates.get_ltceur_buy(),
            'ltceur_sell': rates.get_ltceur_sell(),
    }
    return render(request, 'xbtzmenarenapp/publicRates.html', context)

def rate_btceur_buy(request):
    return HttpResponse(rates.get_btceur_buy())

def rate_btceur_sell(request):
    return HttpResponse(rates.get_btceur_sell())

def rate_ltceur_buy(request):
    return HttpResponse(rates.get_ltceur_buy())

def rate_ltceur_sell(request):
    return HttpResponse(rates.get_ltceur_sell())

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
def withdrawal(request):
    context = {
        'max_sum_eur': request.user.balance.eur,
        'max_sum_btc': request.user.balance.btc,
        'max_sum_ltc': request.user.balance.ltc,
        'fee_btc': 0.0001,
        'fee_ltc': 0.0005,
    }
    return render(request, 'xbtzmenarenapp/withdrawal.html', context)

@login_required
def withdrawal_eur(request):
    sum_eur = request.POST['sum_eur']
    iban = request.POST['account_number']
    return HttpResponse("Withdraw EUR: " + sum_eur + ' to IBAN: ' + iban)

@login_required
def withdrawal_btc(request):
    sum_btc = request.POST['sum_btc']
    address_btc = request.POST['address_btc']
    is_instant = True if 'is_instant_btc' in request.POST else False
    return HttpResponse(
        'Withdraw BTC: ' + sum_btc      \
        + ' to address: ' + address_btc \
        + ' instant: ' + str(is_instant)
    )

@login_required
def withdrawal_ltc(request):
    sum_ltc = request.POST['sum_ltc']
    address_ltc = request.POST['address_ltc']
    is_instant = True if 'is_instant_ltc' in request.POST else False
    return HttpResponse(
        "Withdraw LTC: " + sum_ltc      \
        + ' to address: ' + address_ltc \
        + ' instant: ' + str(is_instant)
    )

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
    return render(request, 'xbtzmenarenapp/managementVerification.html', context)

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
