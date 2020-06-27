from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def buy(request):
    template = loader.get_template('xbtzmenarenapp/buy.html')
    context = {
        'ok_message': "Nakup uspesny",
        'error_message': "Nesapravna hodnota",
        'max_sum_eur': 55,
    }
    return HttpResponse(template.render(context, request))

def buy_btc(request):
    sum_eur = request.POST['sum_eur']
    return HttpResponse("coin: Bitcoin" + "\n"  + "sum: " + sum_eur)

def buy_ltc(request):
    sum_eur = request.POST['sum_eur']
    return HttpResponse("coin: Litecoin" + "\n"  + "sum: " + sum_eur)

def sell(request):
    template = loader.get_template('xbtzmenarenapp/sell.html')
    context = {
        'ok_message': "Predaj uspesny",
        'error_message': "Nesapravna hodnota",
        'max_sum_btc': 0.01,
        'max_sum_ltc': 2,
    }
    return HttpResponse(template.render(context, request))

def sell_btc(request):
    sum_btc = request.POST['sum_btc']
    return HttpResponse("coin: Bitcoin" + "\n"  + "sum: " + sum_btc)

def sell_ltc(request):
    sum_ltc = request.POST['sum_ltc']
    return HttpResponse("coin: Litecoin" + "\n"  + "sum: " + sum_ltc)
