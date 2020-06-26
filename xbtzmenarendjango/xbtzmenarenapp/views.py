from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def buy(request):
    template = loader.get_template('xbtzmenarenapp/buy.html')
    return HttpResponse(template.render({'ok_message': "Nakup uspesny", 'error_message': "Nesapravna hodnota"}, request))

def buy_action(request):
    coin = request.POST['coin_selection']
    sum_eur = request.POST['sum_eur']
    print(coin, sum_eur)
    return HttpResponse("coin: " + coin + "\n"  + "sum: " + sum_eur)
