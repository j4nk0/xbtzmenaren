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

    path('limit-order-buy/', views.limit_order_buy, name='limit-order-buy'),
    path('limit-order-sell/', views.limit_order_sell, name='limit-order-sell'),
    path('limit-order-buy-btc/', views.limit_order_buy_btc, name='limit-order-buy-btc'),
    path('limit-order-buy-btc/json', views.limit_order_buy_btc_json, name='limit-order-buy-btc-json'),
    path('limit-order-buy-ltc/', views.limit_order_buy_ltc, name='limit-order-buy-ltc'),
    path('limit-order-buy-ltc/json', views.limit_order_buy_ltc_json, name='limit-order-buy-ltc-json'),
    path('limit-order-sell-btc/', views.limit_order_sell_btc, name='limit-order-sell-btc'),
    path('limit-order-sell-btc/json', views.limit_order_sell_btc_json, name='limit-order-sell-btc-json'),
    path('limit-order-sell-ltc/', views.limit_order_sell_ltc, name='limit-order-sell-ltc'),
    path('limit-order-sell-ltc/json', views.limit_order_sell_ltc_json, name='limit-order-sell-ltc-json'),

    path('rates/', views.private_rates, name='rates'),
    path('rates/json', views.rates_json, name='rates-json'),
    path('buy-btc/json', views.buy_btc_json, name='buy-btc-json'),
    path('buy-ltc/json', views.buy_ltc_json, name='buy-ltc-json'),
    path('sell-btc/json', views.sell_btc_json, name='sell-btc-json'),
    path('sell-ltc/json', views.sell_ltc_json, name='sell-ltc-json'),

    path('terms/', views.terms_and_conditions, name='terms'),

    path('contacts/', views.contacts, name='contacts'),

    path('registration/', views.registration, name='registration'),
    path('registration-attempt/', views.registration_attempt, name='registration-attempt'),

    path('portfolio/', views.portfolio, name='portfolio'),

    path('change-password/', views.change_password, name='change-password'),
    path('change-password-attempt/', views.change_password_attempt, name='change-password-attempt'),

    path('deposit/', views.deposit, name='deposit'),

    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('withdrawal-eur/', views.withdrawal_eur, name='withdrawal-eur'),
    path('withdrawal-btc/', views.withdrawal_btc, name='withdrawal-btc'),
    path('withdrawal-ltc/', views.withdrawal_ltc, name='withdrawal-ltc'),

    path('management/verification/', views.management_verification, name='management-verification'),
    path('management/verification-attempt/', views.management_verification_attempt, name='management-verification-attempt'),

    path('management/withdrawals/', views.management_withdrawals, name='management-withdrawals'),
    path('management/withdrawal-eur-check/<int:withdrawal_id>', views.management_withdrawal_eur_check, name='management-withdrawal-eur-check'),
    path('management/withdrawal-btc-check/<int:withdrawal_id>', views.management_withdrawal_btc_check, name='management-withdrawal-btc-check'),
    path('management/withdrawal-ltc-check/<int:withdrawal_id>', views.management_withdrawal_ltc_check, name='management-withdrawal-ltc-check'),

    path('management/deposits/', views.management_deposits, name='management-deposits'),
    path('management/deposit-attempt/', views.management_deposit_attempt, name='deposit-eur-attempt'),

    path('management/balances/', views.management_balances, name='management-balances'),

    path('management/buys/', views.management_buys, name='management-buys'),

    path('management/sells/', views.management_sells, name='management-sells'),
]
