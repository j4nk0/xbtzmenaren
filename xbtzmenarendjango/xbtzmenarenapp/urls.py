from django.urls import path

from . import views

urlpatterns = [
    path('', views.buy, name='buy'),
    path('buy/', views.buy, name='buy'),
    path('buy-btc/', views.buy_btc, name='buy-btc'),
    path('buy-ltc/', views.buy_ltc, name='buy-ltc'),
]
