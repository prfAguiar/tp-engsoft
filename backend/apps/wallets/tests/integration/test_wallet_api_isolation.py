from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.wallets.models import Wallet, WalletItem
from apps.wallets.tests.factories import (
    DEFAULT_PASSWORD,
    auth_headers,
    create_investment,
    create_user_with_jwt,
)


class WalletAPIIntegrationTestCase(APITestCase):
    def setUp(self):
        self.wallet_url = reverse('wallet-detail')
        self.items_url = reverse('wallet-item-create')
        self.user, self.access, self.refresh = create_user_with_jwt(email='api@finless.com')
        self.rf = create_investment(name='Tesouro Selic', inv_type='FIXED_INCOME', profitability=Decimal('10.50'))
        self.stock = create_investment(name='Petrobras', inv_type='STOCK', profitability=None)
        self.fii = create_investment(name='Maxi Renda', inv_type='FII', profitability=None)

    def test_all_wallet_endpoints_require_authentication(self):
        self.assertEqual(self.client.get(self.wallet_url).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.post(self.items_url, {}, format='json').status_code, 401)
        self.assertEqual(self.client.delete(reverse('wallet-item-delete', args=[1])).status_code, 401)

    def test_wallet_patch_and_put_return_405_and_preserve_total(self):
        headers = auth_headers(self.access)
        self.assertEqual(self.client.patch(self.wallet_url, {'total_amount': '99999.00'}, format='json', **headers).status_code, 405)
        self.assertEqual(self.client.put(self.wallet_url, {'total_amount': '99999.00'}, format='json', **headers).status_code, 405)
        self.assertEqual(Wallet.objects.get(user=self.user).total_amount, Decimal('0.00'))

    def test_get_empty_wallet_returns_zero_and_empty_items(self):
        res = self.client.get(self.wallet_url, **auth_headers(self.access))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['total_amount'], '0.00')
        self.assertEqual(res.data['items'], [])

    def test_add_multiple_asset_types_and_upsert_with_decimal_precision(self):
        headers = auth_headers(self.access)
        r1 = self.client.post(self.items_url, {'investment': self.rf.pk, 'amount': '100.10'}, format='json', **headers)
        r2 = self.client.post(self.items_url, {'investment': self.rf.pk, 'amount': '200.20'}, format='json', **headers)
        r3 = self.client.post(self.items_url, {'investment': self.stock.pk, 'amount': '50.00'}, format='json', **headers)
        r4 = self.client.post(self.items_url, {'investment': self.fii.pk, 'amount': '0.01'}, format='json', **headers)

        self.assertEqual((r1.status_code, r2.status_code, r3.status_code, r4.status_code), (201, 200, 201, 201))
        res = self.client.get(self.wallet_url, **headers)
        self.assertEqual(res.data['total_amount'], '350.31')
        by_name = {item['investment_name']: item for item in res.data['items']}
        self.assertEqual(by_name['Tesouro Selic']['profitability_estimate'], 10.5)
        self.assertEqual(by_name['Petrobras']['profitability_estimate'], 12.0)
        self.assertEqual(by_name['Maxi Renda']['profitability_estimate'], 9.0)

    def test_add_item_rejects_invalid_amounts_and_nonexistent_investment(self):
        headers = auth_headers(self.access)
        bad_payloads = [
            {'investment': self.rf.pk, 'amount': '0.00'},
            {'investment': self.rf.pk, 'amount': '-10.00'},
            {'investment': self.rf.pk, 'amount': '10.123'},
            {'investment': self.rf.pk, 'amount': '10000000000000.00'},
            {'investment': 999999, 'amount': '100.00'},
            {'investment': self.rf.pk},
            {'amount': '100.00'},
        ]
        for payload in bad_payloads:
            with self.subTest(payload=payload):
                res = self.client.post(self.items_url, payload, format='json', **headers)
                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WalletItem.objects.count(), 0)

    def test_delete_nonexistent_double_delete_and_partial_removal(self):
        headers = auth_headers(self.access)
        i1 = self.client.post(self.items_url, {'investment': self.rf.pk, 'amount': '150.00'}, format='json', **headers).data['id']
        self.client.post(self.items_url, {'investment': self.stock.pk, 'amount': '250.00'}, format='json', **headers)

        self.assertEqual(self.client.delete(reverse('wallet-item-delete', args=[999999]), **headers).status_code, 404)
        self.assertEqual(self.client.delete(reverse('wallet-item-delete', args=[i1]), **headers).status_code, 204)
        self.assertEqual(self.client.delete(reverse('wallet-item-delete', args=[i1]), **headers).status_code, 404)
        self.assertEqual(Wallet.objects.get(user=self.user).total_amount, Decimal('250.00'))

    def test_strict_multi_user_isolation_and_cross_session_persistence(self):
        other_user, other_access, _ = create_user_with_jwt(email='other.wallet@finless.com')
        item_a = self.client.post(
            self.items_url, {'investment': self.rf.pk, 'amount': '400.00'}, format='json', **auth_headers(self.access)
        ).data['id']
        self.client.post(
            self.items_url, {'investment': self.rf.pk, 'amount': '900.00'}, format='json', **auth_headers(other_access)
        )

        self.assertEqual(self.client.delete(reverse('wallet-item-delete', args=[item_a]), **auth_headers(other_access)).status_code, 404)
        self.assertEqual(self.client.get(self.wallet_url, **auth_headers(other_access)).data['total_amount'], '900.00')

        self.client.post(reverse('logout'), {'refresh': self.refresh}, format='json', **auth_headers(self.access))
        relogin = self.client.post(reverse('login'), {'email': 'api@finless.com', 'password': DEFAULT_PASSWORD}, format='json')
        persisted = self.client.get(self.wallet_url, **auth_headers(relogin.data['access']))
        self.assertEqual(persisted.data['total_amount'], '400.00')
        self.assertEqual(len(persisted.data['items']), 1)
