from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.investments.models import Investment


class InvestmentsIntegrationTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.catalog_url = reverse('investment-catalog')
        self.projection_url = reverse('investment-projection')

    def tearDown(self):
        cache.clear()

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_seed_catalog_and_cache_integration(self, mock_sleep, mock_ticker):
        """Integra seed_investments -> banco -> GET /catalog/ -> finance_api -> cache."""
        def fake_ticker(symbol, session=None):
            return MagicMock(info={
                'currentPrice': 25.0,
                'dividendYield': 0.08,
                'currency': 'BRL',
                'longName': symbol,
                'sector': 'Finance',
            })

        mock_ticker.side_effect = fake_ticker
        call_command('seed_investments', stdout=StringIO())

        first_response = self.client.get(self.catalog_url)
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(first_response.data), 10)

        with_ticker = [item for item in first_response.data if item['ticker']]
        without_ticker = [item for item in first_response.data if not item['ticker']]
        self.assertEqual(len(with_ticker), 7)
        self.assertEqual(len(without_ticker), 3)
        self.assertTrue(all(item['live_data']['live_price'] == 25.0 for item in with_ticker))
        self.assertTrue(all(item['live_data'] is None for item in without_ticker))
        self.assertEqual(mock_ticker.call_count, 7)

        # Segunda requisição deve ser 100% atendida pelo cache sem chamar yfinance
        second_response = self.client.get(self.catalog_url)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.data, first_response.data)
        self.assertEqual(mock_ticker.call_count, 7)

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_catalog_resilience_on_partial_external_api_failure(self, mock_sleep, mock_ticker):
        """Falha em um ticker no Yahoo Finance não deve quebrar a listagem do catálogo."""
        def fake_ticker(symbol, session=None):
            if symbol == 'VALE3.SA':
                raise RuntimeError('Rate limited')
            return MagicMock(info={'currentPrice': 38.0, 'dividendYield': 0.1, 'currency': 'BRL'})

        mock_ticker.side_effect = fake_ticker
        Investment.objects.create(name='Petrobras', ticker='PETR4.SA', type='STOCK', risk_level='HIGH', liquidity_deadline=2)
        Investment.objects.create(name='Vale', ticker='VALE3.SA', type='STOCK', risk_level='HIGH', liquidity_deadline=2)
        Investment.objects.create(name='Tesouro Selic', ticker='', type='FIXED_INCOME', risk_level='LOW', profitability=10.5, liquidity_deadline=1)

        response = self.client.get(self.catalog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        by_name = {item['name']: item for item in response.data}
        self.assertEqual(by_name['Petrobras']['live_data']['live_price'], 38.0)
        self.assertEqual(by_name['Vale']['live_data'], {})
        self.assertIsNone(by_name['Tesouro Selic']['live_data'])

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_catalog_to_projection_user_flow(self, mock_sleep, mock_ticker):
        """Fluxo integrado: busca taxa de um ativo de renda fixa no catálogo e projeta ganhos."""
        mock_ticker.return_value = MagicMock(info={'currentPrice': 10.0, 'currency': 'BRL'})
        call_command('seed_investments', stdout=StringIO())

        catalog_resp = self.client.get(self.catalog_url)
        self.assertEqual(catalog_resp.status_code, status.HTTP_200_OK)

        selic = next(item for item in catalog_resp.data if item['name'] == 'Tesouro Selic 2029')
        payload = {
            'initial_amount': 1000.0,
            'monthly_contribution': 0.0,
            'annual_rate': float(selic['profitability']),
            'period_months': 12,
        }
        proj_resp = self.client.post(self.projection_url, payload, format='json')
        self.assertEqual(proj_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(proj_resp.data['final_balance'], 1105.0)
        self.assertEqual(proj_resp.data['total_interest_earned'], 105.0)
