from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.investments.models import Investment
from apps.wallets.models import Wallet, WalletItem

User = get_user_model()


def make_investment(**kwargs):
    defaults = dict(
        name='Tesouro Selic',
        type='FIXED_INCOME',
        risk_level='LOW',
        liquidity_deadline=1,
    )
    defaults.update(kwargs)
    return Investment.objects.create(**defaults)


class WalletTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='wallet_test_user@example.com',
            email='wallet_test_user@example.com',
            password='StrongPassword123!',
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        self.investment = make_investment()

    def test_add_item_creates_and_updates_wallet_total(self):
        url = '/api/wallets/items/'
        res = self.client.post(url, {'investment': self.investment.pk, 'amount': '500.00'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(float(wallet.total_amount), 500.0)

    def test_add_duplicate_investment_upserts_amount(self):
        url = '/api/wallets/items/'
        self.client.post(url, {'investment': self.investment.pk, 'amount': '500.00'})
        res2 = self.client.post(url, {'investment': self.investment.pk, 'amount': '250.00'})
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

        self.assertEqual(WalletItem.objects.filter(wallet__user=self.user).count(), 1)
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(float(wallet.total_amount), 750.0)

    def test_delete_item_decrements_wallet_total(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.user)
        item = WalletItem.objects.create(wallet=wallet, investment=self.investment, amount=400.00)
        wallet.recalculate_total()
        self.assertEqual(float(wallet.total_amount), 400.0)

        del_res = self.client.delete(f'/api/wallets/items/{item.pk}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

        wallet.refresh_from_db()
        self.assertEqual(float(wallet.total_amount), 0.0)

    def test_cannot_delete_other_user_item(self):
        other = User.objects.create_user(
            username='other@example.com', email='other@example.com', password='StrongPassword123!'
        )
        other_wallet, _ = Wallet.objects.get_or_create(user=other)
        other_item = WalletItem.objects.create(wallet=other_wallet, investment=self.investment, amount=100.0)

        del_res = self.client.delete(f'/api/wallets/items/{other_item.pk}/')
        self.assertEqual(del_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_wallet_returns_items_and_total(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.user)
        WalletItem.objects.create(wallet=wallet, investment=self.investment, amount=150.00)

        res = self.client.get('/api/wallets/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(float(res.data['total_amount']), 150.00)
        self.assertEqual(len(res.data['items']), 1)
