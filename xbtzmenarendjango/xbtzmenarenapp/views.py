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
