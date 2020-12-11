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

class Deposit_eurAdmin(admin.ModelAdmin):
    list_display = ('user', 'vs', 'eur', 'datetime',)
    search_fields = ('user', 'vs', 'eur', 'datetime',)

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
admin.site.register(Questionare, QuestionareAdmin)

admin.site.register(Withdrawal_eur, Withdrawal_eurAdmin)
admin.site.register(Deposit_eur, Deposit_eurAdmin)

#======================= Generated code below: =======================#

for c in CURRENCIES:
    exec('''
class Withdrawal_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', 'time_created', 'time_processed', 'address', "''' + c + '''", 'is_pending')
    search_fields = ('address', "''' + c + '''",)
    list_filter = ('is_pending',)

class Buy_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', 'datetime', "''' + c + '''", 'eur',)
    search_fields = ('user', "''' + c + '''", 'eur')

class Sell_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', 'datetime', "''' + c + '''", 'eur',)
    search_fields = ('user', "''' + c + '''", 'eur')

class Deposit_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', 'address', "''' + c + '''", 'datetime',)
    search_fields = ('user', 'address', "''' + c + '''", 'datetime',)

class Order_buy_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', "''' + c + '''", 'price', 'datetime',)
    search_fields = ('user', "''' + c + '''", 'price', 'datetime',)

class Order_sell_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', "''' + c + '''", 'price', 'datetime',)
    search_fields = ('user', "''' + c + '''", 'price', 'datetime',)

class Incoming_''' + c + '''Admin(admin.ModelAdmin):
    list_display = ('user', 'address', "''' + c + '''", 'confirmations', 'txid')
    search_fields = ('user', 'address', "''' + c + '''", 'confirmations', 'txid')


admin.site.register(Withdrawal_''' + c + ''', Withdrawal_''' + c + '''Admin)
admin.site.register(Buy_''' + c + ''', Buy_''' + c + '''Admin)
admin.site.register(Sell_''' + c + ''', Sell_''' + c + '''Admin)
admin.site.register(Deposit_''' + c + ''', Deposit_''' + c + '''Admin)
admin.site.register(Order_buy_''' + c + ''', Order_buy_''' + c + '''Admin)
admin.site.register(Order_sell_''' + c + ''', Order_sell_''' + c + '''Admin)
admin.site.register(Incoming_''' + c + ''', Incoming_''' + c + '''Admin)
''')

