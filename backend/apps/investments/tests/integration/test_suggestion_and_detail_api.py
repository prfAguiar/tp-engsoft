from decimal import Decimal
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.investments.models import Investment
from apps.wallets.models import WalletItem
from apps.wallets.tests.factories import auth_headers, create_investment, create_user_with_jwt


class SuggestionAndDetailAPIIntegrationTestCase(APITestCase):
    def setUp(self):
        self.suggest_url = reverse('investment-suggestion')

    def test_suggestion_authenticated_rebalances_existing_wallet_and_uses_db_catalog(self):
        user, access, _ = create_user_with_jwt(
            email='rebalance.api@finless.com',
            investor_profile='MODERATE',
        )
        selic = create_investment(name='Tesouro Selic', inv_type='FIXED_INCOME')
        fii = create_investment(name='Maxi Renda', inv_type='FII', ticker='MXRF11.SA')
        stock = create_investment(name='Itaú Unibanco', inv_type='STOCK', ticker='ITUB4.SA')
        WalletItem.objects.create(wallet=user.wallet, investment=selic, amount=Decimal('10000.00'))

        response = self.client.post(
            self.suggest_url,
            {'amount': 5000.0},
            format='json',
            **auth_headers(access),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['rebalanced'])
        self.assertEqual(response.data['current_portfolio_total'], 10000.0)

        by_type = {item['type']: item for item in response.data['allocations']}
        self.assertEqual(by_type['FIXED_INCOME']['allocated_amount'], 0.0)
        self.assertIn('Maxi Renda (MXRF11.SA)', by_type['FII']['suggested_assets'])
        self.assertIn('Itaú Unibanco (ITUB4.SA)', by_type['STOCK']['suggested_assets'])

    def test_suggestion_returns_400_when_user_carries_unrecognized_profile(self):
        user, access, _ = create_user_with_jwt(
            email='corrupt.profile@finless.com',
            investor_profile='UNKNOWN_PROFILE',
        )
        response = self.client.post(
            self.suggest_url,
            {'amount': 2500.0},
            format='json',
            **auth_headers(access),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('apps.investments.serializers.get_live_asset_data')
    def test_investment_detail_endpoint_returns_asset_and_404_when_missing(self, mock_live):
        mock_live.return_value = {'live_price': 34.50, 'currency': 'BRL'}
        asset = Investment.objects.create(
            name='Petrobras',
            ticker='PETR4.SA',
            type='STOCK',
            risk_level='HIGH',
            liquidity_deadline=2,
            description='Ação ordinária',
        )

        detail_url = reverse('investment-detail', kwargs={'pk': asset.pk})
        res_ok = self.client.get(detail_url)
        self.assertEqual(res_ok.status_code, status.HTTP_200_OK)
        self.assertEqual(res_ok.data['name'], 'Petrobras')
        self.assertEqual(res_ok.data['live_data']['live_price'], 34.50)

        missing_url = reverse('investment-detail', kwargs={'pk': 999999})
        res_404 = self.client.get(missing_url)
        self.assertEqual(res_404.status_code, status.HTTP_404_NOT_FOUND)
