from django.urls import path

from . import views

urlpatterns = [
    path('', views.public_rates, name='public-rates'),

    path('buy/', views.buy, name='buy'),
    path('buy-btc/', views.buy_btc, name='buy-btc'),
    path('buy-ltc/', views.buy_ltc, name='buy-ltc'),

    path('sell/', views.sell, name='sell'),
    path('sell-btc/', views.sell_btc, name='sell-btc'),
    path('sell-ltc/', views.sell_ltc, name='sell-ltc'),

    path('rates/', views.private_rates, name='rates'),
    path('rate-btceur-buy/', views.rate_btceur_buy, name='rate-btceur-buy'),
    path('rate-btceur-sell/', views.rate_btceur_sell, name='rate-btceur-sell'),
    path('rate-ltceur-buy/', views.rate_ltceur_buy, name='rate-ltceur-buy'),
    path('rate-ltceur-sell/', views.rate_ltceur_sell, name='rate-ltceur-sell'),

    path('terms/', views.terms_and_conditions, name='terms'),
    path('contacts/', views.contacts, name='contacts'),

    path('registration/', views.registration, name='registration'),
    path('registration-attempt/', views.registration_attempt, name='registration-attempt'),

    path('portfolio/', views.portfolio, name='portfolio'),
]
