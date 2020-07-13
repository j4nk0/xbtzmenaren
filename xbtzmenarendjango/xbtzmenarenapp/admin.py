from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, Balance, Withdrawal_eur

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

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Withdrawal_eur, Withdrawal_eurAdmin)

