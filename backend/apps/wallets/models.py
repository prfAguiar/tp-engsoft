from django.db import models
from django.conf import settings
from apps.investments.models import Investment

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.user.email}"

    def recalculate_total(self):
        from django.db.models import Sum
        total = self.items.aggregate(total=Sum('amount'))['total'] or 0.00
        self.total_amount = total
        self.save(update_fields=['total_amount', 'updated_at'])
        return total

class WalletItem(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='items')
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} in {self.investment.name} (Wallet: {self.wallet.user.email})"
