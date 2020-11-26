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
    list_display = ('user', 'vs', 'btc', 'ltc',)
    search_fields = ('vs',)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'eur', 'btc', 'ltc',)
    search_fields = ('eur', 'btc', 'ltc')

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

class Deposit_eurAdmin(admin.ModelAdmin):
    list_display = ('user', 'vs', 'eur', 'datetime',)
    search_fields = ('user', 'vs', 'eur', 'datetime',)

class Deposit_btcAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'btc', 'datetime',)
    search_fields = ('user', 'address', 'btc', 'datetime',)

class Deposit_ltcAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'ltc', 'datetime',)
    search_fields = ('user', 'address', 'ltc', 'datetime',)

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

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Withdrawal_eur, Withdrawal_eurAdmin)
admin.site.register(Withdrawal_btc, Withdrawal_btcAdmin)
admin.site.register(Withdrawal_ltc, Withdrawal_ltcAdmin)
admin.site.register(Buy_btc, Buy_btcAdmin)
admin.site.register(Sell_btc, Sell_btcAdmin)
admin.site.register(Buy_ltc, Buy_ltcAdmin)
admin.site.register(Sell_ltc, Sell_ltcAdmin)
admin.site.register(Deposit_eur, Deposit_eurAdmin)
admin.site.register(Deposit_btc, Deposit_btcAdmin)
admin.site.register(Deposit_ltc, Deposit_ltcAdmin)
admin.site.register(Order_buy_btc, Order_buy_btcAdmin)
admin.site.register(Order_sell_btc, Order_sell_btcAdmin)
admin.site.register(Order_buy_ltc, Order_buy_ltcAdmin)
admin.site.register(Order_sell_ltc, Order_sell_ltcAdmin)

