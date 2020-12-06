from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'is_superuser', 'is_staff', 'is_active', 'is_verified',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_verified',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active', 'is_verified')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'vs', 'btc', 'ltc', 'doge',)
    search_fields = ('vs',)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'eur', 'btc', 'ltc', 'doge',)
    search_fields = ('eur', 'btc', 'ltc', 'doge',)

class Withdrawal_eurAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_created', 'time_processed', 'iban', 'eur', 'is_pending')
    search_fields = ('iban', 'eur',)
    list_filter = ('is_pending',)

class Withdrawal_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_created', 'time_processed', 'address', 'btc', 'is_pending')
    search_fields = ('address', 'btc',)
    list_filter = ('is_pending',)

class Withdrawal_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_created', 'time_processed', 'address', 'ltc', 'is_pending')
    search_fields = ('address', 'ltc',)
    list_filter = ('is_pending',)

class Withdrawal_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_created', 'time_processed', 'address', 'doge', 'is_pending')
    search_fields = ('address', 'doge',)
    list_filter = ('is_pending',)

class Buy_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'btc', 'eur',)
    search_fields = ('user', 'btc', 'eur')

class Sell_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'btc', 'eur',)
    search_fields = ('user', 'btc', 'eur')

class Buy_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'ltc', 'eur',)
    search_fields = ('user', 'ltc', 'eur')

class Sell_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'ltc', 'eur',)
    search_fields = ('user', 'ltc', 'eur')

class Buy_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'doge', 'eur',)
    search_fields = ('user', 'doge', 'eur')

class Sell_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'doge', 'eur',)
    search_fields = ('user', 'doge', 'eur')

class Deposit_eurAdmin(admin.ModelAdmin):
    list_display = ('user', 'vs', 'eur', 'datetime',)
    search_fields = ('user', 'vs', 'eur', 'datetime',)

class Deposit_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'btc', 'datetime',)
    search_fields = ('user', 'address', 'btc', 'datetime',)

class Deposit_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'ltc', 'datetime',)
    search_fields = ('user', 'address', 'ltc', 'datetime',)

class Deposit_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'doge', 'datetime',)
    search_fields = ('user', 'address', 'doge', 'datetime',)

class Order_buy_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'btc', 'price', 'datetime',)
    search_fields = ('user', 'btc', 'price', 'datetime',)

class Order_sell_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'btc', 'price', 'datetime',)
    search_fields = ('user', 'btc', 'price', 'datetime',)

class Order_buy_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'ltc', 'price', 'datetime',)
    search_fields = ('user', 'ltc', 'price', 'datetime',)

class Order_sell_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'ltc', 'price', 'datetime',)
    search_fields = ('user', 'ltc', 'price', 'datetime',)

class Order_buy_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'doge', 'price', 'datetime',)
    search_fields = ('user', 'doge', 'price', 'datetime',)

class Order_sell_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'doge', 'price', 'datetime',)
    search_fields = ('user', 'doge', 'price', 'datetime',)

class Incoming_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'btc', 'confirmations', 'txid')
    search_fields = ('user', 'address', 'btc', 'confirmations', 'txid')

class Incoming_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'ltc', 'confirmations', 'txid')
    search_fields = ('user', 'address', 'ltc', 'confirmations', 'txid')

class Incoming_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'doge', 'confirmations', 'txid')
    search_fields = ('user', 'address', 'doge', 'confirmations', 'txid')

class QuestionareAdmin(admin.ModelAdmin):
    list_display = ('user',
        'question1', 'question2', 'question3', 'question4', \
        'question5', 'question6', 'question7', 'question8', \
        'question9', 'question10'
    )
    search_fields = ('user',
        'question1', 'question2', 'question3', 'question4', \
        'question5', 'question6', 'question7', 'question8', \
        'question9', 'question10'
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Withdrawal_eur, Withdrawal_eurAdmin)
admin.site.register(Withdrawal_btc, Withdrawal_btcAdmin)
admin.site.register(Withdrawal_ltc, Withdrawal_ltcAdmin)
admin.site.register(Withdrawal_doge, Withdrawal_dogeAdmin)
admin.site.register(Buy_btc, Buy_btcAdmin)
admin.site.register(Sell_btc, Sell_btcAdmin)
admin.site.register(Buy_ltc, Buy_ltcAdmin)
admin.site.register(Sell_ltc, Sell_ltcAdmin)
admin.site.register(Buy_doge, Buy_dogeAdmin)
admin.site.register(Sell_doge, Sell_dogeAdmin)
admin.site.register(Deposit_eur, Deposit_eurAdmin)
admin.site.register(Deposit_btc, Deposit_btcAdmin)
admin.site.register(Deposit_ltc, Deposit_ltcAdmin)
admin.site.register(Deposit_doge, Deposit_dogeAdmin)
admin.site.register(Order_buy_btc, Order_buy_btcAdmin)
admin.site.register(Order_sell_btc, Order_sell_btcAdmin)
admin.site.register(Order_buy_ltc, Order_buy_ltcAdmin)
admin.site.register(Order_sell_ltc, Order_sell_ltcAdmin)
admin.site.register(Order_buy_doge, Order_buy_dogeAdmin)
admin.site.register(Order_sell_doge, Order_sell_dogeAdmin)
admin.site.register(Incoming_btc, Incoming_btcAdmin)
admin.site.register(Incoming_ltc, Incoming_ltcAdmin)
admin.site.register(Incoming_doge, Incoming_dogeAdmin)
admin.site.register(Questionare, QuestionareAdmin)

