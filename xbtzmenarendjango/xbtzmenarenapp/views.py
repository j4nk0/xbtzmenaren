from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def buy(request):
    template = loader.get_template('xbtzmenarenapp/buy.html')
    return HttpResponse(template.render({}, request))

def buy_action(request):
    coin = request.POST['coin_sel']
    sum_eur = request.POST['sum']
    print(coin, sum_eur)
    return HttpResponse("coin: " + coin + "sum: " + sum_eur)
