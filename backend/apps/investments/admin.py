from django.contrib import admin
from .models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'type', 'risk_level', 'profitability', 'liquidity_deadline')
    list_filter = ('type', 'risk_level')
    search_fields = ('name', 'ticker')
