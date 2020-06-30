from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('buy/', views.buy, name='buy'),
    path('buy-btc/', views.buy_btc, name='buy-btc'),
    path('buy-ltc/', views.buy_ltc, name='buy-ltc'),

    path('sell/', views.sell, name='sell'),
    path('sell-btc/', views.sell_btc, name='sell-btc'),
    path('sell-ltc/', views.sell_ltc, name='sell-ltc'),

    path('rates/', views.rates, name='rates'),
]
