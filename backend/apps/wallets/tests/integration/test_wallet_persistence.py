from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.wallets.models import Wallet, WalletItem
from apps.wallets.tests.factories import (
    auth_headers,
    create_investment,
    create_user_with_jwt,
    create_wallet_item,
)


class WalletPersistenceAndSignalsIntegrationTestCase(APITestCase):
    def setUp(self):
        self.wallet_url = reverse('wallet-detail')
        self.items_url = reverse('wallet-item-create')
        self.user, self.access, _ = create_user_with_jwt(email='persist@finless.com')
        self.wallet = Wallet.objects.get(user=self.user)
        self.inv_a = create_investment(name='Selic A', profitability=Decimal('10.50'))
        self.inv_b = create_investment(name='PETR4', inv_type='STOCK', profitability=None)

    def test_user_creation_auto_creates_wallet_and_update_preserves_it(self):
        create_wallet_item(self.wallet, self.inv_a, amount=Decimal('300.00'))
        self.user.first_name = 'Atualizado'
        self.user.save()

        self.assertEqual(Wallet.objects.filter(user=self.user).count(), 1)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, Decimal('300.00'))

    def test_orm_item_create_update_delete_synchronizes_wallet_total(self):
        item = create_wallet_item(self.wallet, self.inv_a, amount=Decimal('120.50'))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, Decimal('120.50'))

        item.amount = Decimal('345.75')
        item.save()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, Decimal('345.75'))

        item.delete()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, Decimal('0.00'))

    def test_deleting_investment_cascades_items_and_recalculates_affected_wallets(self):
        other_user, _, _ = create_user_with_jwt(email='affected@finless.com')
        other_wallet = Wallet.objects.get(user=other_user)

        create_wallet_item(self.wallet, self.inv_a, amount=Decimal('200.00'))
        create_wallet_item(self.wallet, self.inv_b, amount=Decimal('350.00'))
        create_wallet_item(other_wallet, self.inv_b, amount=Decimal('500.00'))

        self.inv_b.delete()

        self.wallet.refresh_from_db()
        other_wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, Decimal('200.00'))
        self.assertEqual(other_wallet.total_amount, Decimal('0.00'))
        self.assertEqual(WalletItem.objects.filter(wallet=other_wallet).count(), 0)

    def test_deleting_user_cascades_wallet_and_items_cleanly(self):
        create_wallet_item(self.wallet, self.inv_a, amount=Decimal('400.00'))
        wallet_pk = self.wallet.pk
        self.user.delete()

        self.assertFalse(Wallet.objects.filter(pk=wallet_pk).exists())
        self.assertEqual(WalletItem.objects.filter(wallet_id=wallet_pk).count(), 0)

    def test_wallet_self_heals_via_get_or_create_when_missing_on_get_and_post(self):
        Wallet.objects.filter(user=self.user).delete()
        res_get = self.client.get(self.wallet_url, **auth_headers(self.access))
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_get.data['total_amount'], '0.00')
        self.assertTrue(Wallet.objects.filter(user=self.user).exists())

        Wallet.objects.filter(user=self.user).delete()
        res_post = self.client.post(
            self.items_url,
            {'investment': self.inv_a.pk, 'amount': '85.25'},
            format='json',
            **auth_headers(self.access),
        )
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.get(user=self.user).total_amount, Decimal('85.25'))
