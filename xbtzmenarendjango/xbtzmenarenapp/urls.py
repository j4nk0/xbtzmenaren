from django.urls import path

from . import views

urlpatterns = [
    path('', views.public_rates, name='public-rates'),

    path('wait/', views.wait_for_verification, name='wait'),

    path('buy/', views.buy, name='buy'),
    path('buy-btc/', views.buy_btc, name='buy-btc'),
    path('buy-ltc/', views.buy_ltc, name='buy-ltc'),
    path('buy-doge/', views.buy_doge, name='buy-doge'),
    path('buy-eth/', views.buy_eth, name='buy-eth'),
    path('buy-xlm/', views.buy_xlm, name='buy-xlm'),
    path('buy-zrx/', views.buy_zrx, name='buy-zrx'),

    path('sell/', views.sell, name='sell'),
    path('sell-btc/', views.sell_btc, name='sell-btc'),
    path('sell-ltc/', views.sell_ltc, name='sell-ltc'),
    path('sell-doge/', views.sell_doge, name='sell-doge'),
    path('sell-eth/', views.sell_eth, name='sell-eth'),
    path('sell-xlm/', views.sell_xlm, name='sell-xlm'),
    path('sell-zrx/', views.sell_zrx, name='sell-zrx'),

    path('limit-order-buy/', views.limit_order_buy, name='limit-order-buy'),
    path('limit-order-sell/', views.limit_order_sell, name='limit-order-sell'),
    path('limit-order-buy-btc/', views.limit_order_buy_btc, name='limit-order-buy-btc'),
    path('limit-order-buy-btc/json', views.limit_order_buy_btc_json, name='limit-order-buy-btc-json'),
    path('limit-order-buy-ltc/', views.limit_order_buy_ltc, name='limit-order-buy-ltc'),
    path('limit-order-buy-ltc/json', views.limit_order_buy_ltc_json, name='limit-order-buy-ltc-json'),
    path('limit-order-buy-doge/', views.limit_order_buy_doge, name='limit-order-buy-doge'),
    path('limit-order-buy-doge/json', views.limit_order_buy_doge_json, name='limit-order-buy-doge-json'),
    path('limit-order-buy-eth/', views.limit_order_buy_eth, name='limit-order-buy-eth'),
    path('limit-order-buy-eth/json', views.limit_order_buy_eth_json, name='limit-order-buy-eth-json'),
    path('limit-order-buy-xlm/', views.limit_order_buy_xlm, name='limit-order-buy-xlm'),
    path('limit-order-buy-xlm/json', views.limit_order_buy_xlm, name='limit-order-buy-xlm-json'),
    path('limit-order-buy-zrx/', views.limit_order_buy_zrx, name='limit-order-buy-zrx'),
    path('limit-order-buy-zrx/json', views.limit_order_buy_zrx_json, name='limit-order-buy-zrx-json'),

    path('limit-order-sell-btc/', views.limit_order_sell_btc, name='limit-order-sell-btc'),
    path('limit-order-sell-btc/json', views.limit_order_sell_btc_json, name='limit-order-sell-btc-json'),
    path('limit-order-sell-ltc/', views.limit_order_sell_ltc, name='limit-order-sell-ltc'),
    path('limit-order-sell-ltc/json', views.limit_order_sell_ltc_json, name='limit-order-sell-ltc-json'),
    path('limit-order-sell-doge/', views.limit_order_sell_doge, name='limit-order-sell-doge'),
    path('limit-order-sell-doge/json', views.limit_order_sell_doge_json, name='limit-order-sell-doge-json'),
    path('limit-order-sell-eth/', views.limit_order_sell_eth, name='limit-order-sell-eth'),
    path('limit-order-sell-eth/json', views.limit_order_sell_eth_json, name='limit-order-sell-eth-json'),
    path('limit-order-sell-xlm/', views.limit_order_sell_xlm, name='limit-order-sell-xlm'),
    path('limit-order-sell-xlm/json', views.limit_order_sell_xlm_json, name='limit-order-sell-xlm-json'),
    path('limit-order-sell-zrx/', views.limit_order_sell_zrx, name='limit-order-sell-zrx'),
    path('limit-order-sell-zrx/json', views.limit_order_sell_zrx_json, name='limit-order-sell-zrx-json'),

    path('limit-order-buy-btc-delete/<int:order_id>', views.limit_order_buy_btc_delete, name='limit-order-buy-btc-delete'),
    path('limit-order-buy-ltc-delete/<int:order_id>', views.limit_order_buy_ltc_delete, name='limit-order-buy-ltc-delete'),
    path('limit-order-buy-doge-delete/<int:order_id>', views.limit_order_buy_doge_delete, name='limit-order-buy-doge-delete'),
    path('limit-order-buy-eth-delete/<int:order_id>', views.limit_order_buy_eth_delete, name='limit-order-buy-eth-delete'),
    path('limit-order-buy-xlm-delete/<int:order_id>', views.limit_order_buy_xlm_delete, name='limit-order-buy-xlm-delete'),
    path('limit-order-buy-zrx-delete/<int:order_id>', views.limit_order_buy_zrx_delete, name='limit-order-buy-zrx-delete'),

    path('limit-order-sell-btc-delete/<int:order_id>', views.limit_order_sell_btc_delete, name='limit-order-sell-btc-delete'),
    path('limit-order-sell-ltc-delete/<int:order_id>', views.limit_order_sell_ltc_delete, name='limit-order-sell-ltc-delete'),
    path('limit-order-sell-doge-delete/<int:order_id>', views.limit_order_sell_doge_delete, name='limit-order-sell-doge-delete'),
    path('limit-order-sell-eth-delete/<int:order_id>', views.limit_order_sell_eth_delete, name='limit-order-sell-eth-delete'),
    path('limit-order-sell-xlm-delete/<int:order_id>', views.limit_order_sell_xlm_delete, name='limit-order-sell-xlm-delete'),
    path('limit-order-sell-zrx-delete/<int:order_id>', views.limit_order_sell_zrx_delete, name='limit-order-sell-zrx-delete'),

    path('rates/', views.private_rates, name='rates'),
    path('rates/json', views.rates_json, name='rates-json'),
    path('buy-btc/json', views.buy_btc_json, name='buy-btc-json'),
    path('buy-ltc/json', views.buy_ltc_json, name='buy-ltc-json'),
    path('buy-doge/json', views.buy_doge_json, name='buy-doge-json'),
    path('buy-eth/json', views.buy_eth_json, name='buy-eth-json'),
    path('buy-xlm/json', views.buy_xlm_json, name='buy-xlm-json'),
    path('buy-zrx/json', views.buy_zrx_json, name='buy-zrx-json'),

    path('sell-btc/json', views.sell_btc_json, name='sell-btc-json'),
    path('sell-ltc/json', views.sell_ltc_json, name='sell-ltc-json'),
    path('sell-doge/json', views.sell_doge_json, name='sell-doge-json'),
    path('sell-eth/json', views.sell_eth_json, name='sell-eth-json'),
    path('sell-xlm/json', views.sell_xlm_json, name='sell-xlm-json'),
    path('sell-zrx/json', views.sell_zrx_json, name='sell-zrx-json'),

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
    path('withdrawal-doge/', views.withdrawal_doge, name='withdrawal-doge'),
    path('withdrawal-eth/', views.withdrawal_eth, name='withdrawal-eth'),
    path('withdrawal-xlm/', views.withdrawal_xlm, name='withdrawal-xlm'),
    path('withdrawal-zrx/', views.withdrawal_zrx, name='withdrawal-zrx'),

    path('management/verification/', views.management_verification, name='management-verification'),
    path('management/verification-attempt/', views.management_verification_attempt, name='management-verification-attempt'),

    path('management/withdrawals/', views.management_withdrawals, name='management-withdrawals'),
    path('management/withdrawal-eur-check/<int:withdrawal_id>', views.management_withdrawal_eur_check, name='management-withdrawal-eur-check'),
    path('management/withdrawal-btc-check/<int:withdrawal_id>', views.management_withdrawal_btc_check, name='management-withdrawal-btc-check'),
    path('management/withdrawal-ltc-check/<int:withdrawal_id>', views.management_withdrawal_ltc_check, name='management-withdrawal-ltc-check'),
    path('management/withdrawal-doge-check/<int:withdrawal_id>', views.management_withdrawal_doge_check, name='management-withdrawal-doge-check'),
    path('management/withdrawal-eth-check/<int:withdrawal_id>', views.management_withdrawal_eth_check, name='management-withdrawal-eth-check'),
    path('management/withdrawal-xlm-check/<int:withdrawal_id>', views.management_withdrawal_xlm_check, name='management-withdrawal-xlm-check'),
    path('management/withdrawal-zrx-check/<int:withdrawal_id>', views.management_withdrawal_zrx_check, name='management-withdrawal-zrx-check'),

    path('management/deposits/', views.management_deposits, name='management-deposits'),
    path('management/deposit-attempt/', views.management_deposit_attempt, name='deposit-eur-attempt'),

    path('management/balances/', views.management_balances, name='management-balances'),

    path('management/buys/', views.management_buys, name='management-buys'),

    path('management/sells/', views.management_sells, name='management-sells'),

    path('management/orderbook/', views.management_orderbook, name='management-orderbook'),
]
