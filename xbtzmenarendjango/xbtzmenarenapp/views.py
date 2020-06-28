from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

def index(request):
    return redirect('auth/login')

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

def buy_btc(request):
    sum_eur = request.POST['sum_eur']
    #return HttpResponse("coin: Bitcoin" + "\n"  + "sum: " + sum_eur)
    return buy(request, True)

def buy_ltc(request):
    sum_eur = request.POST['sum_eur']
    return HttpResponse("coin: Litecoin" + "\n"  + "sum: " + sum_eur)

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

def sell_btc(request):
    sum_btc = request.POST['sum_btc']
    return HttpResponse("coin: Bitcoin" + "\n"  + "sum: " + sum_btc)

def sell_ltc(request):
    sum_ltc = request.POST['sum_ltc']
    return HttpResponse("coin: Litecoin" + "\n"  + "sum: " + sum_ltc)
