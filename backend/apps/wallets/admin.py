from django.contrib import admin
from .models import Wallet, WalletItem


class WalletItemInline(admin.TabularInline):
    model = WalletItem
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'updated_at')
    search_fields = ('user__email',)
    inlines = (WalletItemInline,)


@admin.register(WalletItem)
class WalletItemAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'investment', 'amount', 'created_at')
    list_filter = ('investment__type',)
    search_fields = ('wallet__user__email', 'investment__name')
