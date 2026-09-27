from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Wallet, WalletItem

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=WalletItem)
@receiver(post_delete, sender=WalletItem)
def update_wallet_total_on_item_change(sender, instance, **kwargs):
    if instance.wallet_id:
        instance.wallet.recalculate_total()
