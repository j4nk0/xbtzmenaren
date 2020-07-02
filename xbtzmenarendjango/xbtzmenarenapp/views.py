from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from . import rates

def index(request):
    return redirect('login')

@login_required
def buy(request, success=None):
    context = {
        'max_sum_eur': 55,
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
        'max_sum_btc': 0.01,
        'max_sum_ltc': 2,
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
