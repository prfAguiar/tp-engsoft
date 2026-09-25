from django.db import models

class Investment(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=20, null=True, blank=True, help_text="Ticker B3 (ex: PETR4.SA, MXRF11.SA)")
    type = models.CharField(max_length=50, help_text="FIXED_INCOME, STOCK, FII, etc")
    risk_level = models.CharField(max_length=20)
    profitability = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Rentabilidade fixa se não houver ticker")
    liquidity_deadline = models.IntegerField(help_text="Prazo em dias")
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ticker or self.type})"
