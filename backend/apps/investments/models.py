from django.db import models

class Investment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=20)
    profitability = models.DecimalField(max_digits=5, decimal_places=2)
    liquidity_deadline = models.IntegerField(help_text="Prazo em dias")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
