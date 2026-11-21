from unittest.mock import MagicMock, patch

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .finance_api import get_live_asset_data
from .models import Investment
from .serializers import InvestmentSerializer
from .services import calculate_projection


class InvestmentProjectionServiceTestCase(TestCase):
    def test_calculate_projection_basic(self):
        """Testa se a projeção de rendimentos faz os cálculos corretos."""
        result = calculate_projection(
            initial_amount=1000.0,
            monthly_contribution=100.0,
            annual_rate=12.0,
            period_months=12,
        )

        self.assertEqual(result['initial_amount'], 1000.0)
        self.assertEqual(result['period_months'], 12)
        self.assertEqual(len(result['evolution']), 12)

        # O saldo final deve ser maior que o total aportado sem juros (1000 + 12*100 = 2200)
        self.assertGreater(result['final_balance'], 2200.0)
        self.assertGreater(result['total_interest_earned'], 0.0)

    def test_calculate_projection_zero_contribution(self):
        """Testa se a projeção funciona apenas com montante inicial e juros compostos."""
        result = calculate_projection(
            initial_amount=1000.0,
            monthly_contribution=0.0,
            annual_rate=10.0,
            period_months=12,
        )

        # Com taxa anual de 10%, a taxa mensal equivalente é (1.10)^(1/12) - 1.
        # Após 12 meses: 1000 * ((1.10^(1/12))^12) = 1000 * 1.10 = R$ 1100.00 exato.
        self.assertEqual(round(result['final_balance'], 2), 1100.0)
        self.assertEqual(round(result['total_interest_earned'], 2), 100.0)

        # Garante que é JUROS COMPOSTOS e não simples:
        # Em 24 meses com juros simples seria R$ 1200 (2 × 10% × 1000).
        # Com juros compostos deve ser R$ 1210 (1000 × 1.10²), logo > 1200.
        result_24m = calculate_projection(
            initial_amount=1000.0,
            monthly_contribution=0.0,
            annual_rate=10.0,
            period_months=24,
        )
        self.assertGreater(result_24m['final_balance'], 1200.0)
        self.assertEqual(round(result_24m['final_balance'], 2), 1210.0)

    def test_calculate_projection_zero_annual_rate(self):
        """Com taxa anual de 0%, o saldo final deve ser exatamente igual ao total investido."""
        result = calculate_projection(
            initial_amount=1000.0,
            monthly_contribution=200.0,
            annual_rate=0.0,
            period_months=6,
        )

        self.assertEqual(result['total_contributions'], 1200.0)
        self.assertEqual(result['total_invested'], 2200.0)
        self.assertEqual(result['total_interest_earned'], 0.0)
        self.assertEqual(result['final_balance'], 2200.0)

    def test_calculate_projection_zero_initial_with_contributions(self):
        """Testa projeção começando do zero apenas com aportes mensais."""
        result = calculate_projection(
            initial_amount=0.0,
            monthly_contribution=500.0,
            annual_rate=12.0,
            period_months=12,
        )

        self.assertEqual(result['initial_amount'], 0.0)
        self.assertEqual(result['total_contributions'], 6000.0)
        self.assertEqual(result['total_invested'], 6000.0)
        self.assertGreater(result['total_interest_earned'], 0.0)
        self.assertGreater(result['final_balance'], 6000.0)

    def test_calculate_projection_single_month_and_evolution_consistency(self):
        """Testa período mínimo (1 mês) e consistência dos campos de evolução."""
        result = calculate_projection(
            initial_amount=1000.0,
            monthly_contribution=100.0,
            annual_rate=12.0,
            period_months=1,
        )

        self.assertEqual(len(result['evolution']), 1)
        entry = result['evolution'][0]
        self.assertEqual(entry['month'], 1)
        self.assertEqual(entry['invested_amount'], 1100.0)
        self.assertEqual(entry['total_balance'], result['final_balance'])
        self.assertAlmostEqual(
            entry['invested_amount'] + entry['interest_earned'],
            entry['total_balance'],
            places=2,
        )

    def test_calculate_projection_evolution_is_monotonic(self):
        """Verifica que os meses são sequenciais e saldo/aportes crescem mês a mês."""
        result = calculate_projection(
            initial_amount=500.0,
            monthly_contribution=100.0,
            annual_rate=10.0,
            period_months=6,
        )

        months = [item['month'] for item in result['evolution']]
        self.assertEqual(months, [1, 2, 3, 4, 5, 6])

        for i in range(1, len(result['evolution'])):
            prev = result['evolution'][i - 1]
            curr = result['evolution'][i]
            self.assertGreater(curr['invested_amount'], prev['invested_amount'])
            self.assertGreater(curr['total_balance'], prev['total_balance'])


class InvestmentProjectionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('investment-projection')

    def test_projection_endpoint_success(self):
        """Testa requisição POST com sucesso no endpoint /api/investments/projection/."""
        payload = {
            "initial_amount": 5000.0,
            "monthly_contribution": 500.0,
            "annual_rate": 10.5,
            "period_months": 24,
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('final_balance', response.data)
        self.assertIn('evolution', response.data)
        self.assertEqual(len(response.data['evolution']), 24)

    def test_projection_endpoint_defaults(self):
        """Quando initial_amount e monthly_contribution são omitidos, devem assumir 0.0."""
        payload = {
            "annual_rate": 10.0,
            "period_months": 12,
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['initial_amount'], 0.0)
        self.assertEqual(response.data['total_contributions'], 0.0)
        self.assertEqual(response.data['final_balance'], 0.0)

    def test_projection_endpoint_validation_error(self):
        """Testa se dados inválidos retornam HTTP 400 Bad Request."""
        payload = {
            "initial_amount": -100.0,  # Inválido (menor que 0)
            "annual_rate": 150.0,     # Inválido (maior que 100)
            "period_months": 0,       # Inválido (menor que 1)
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('initial_amount', response.data)
        self.assertIn('annual_rate', response.data)
        self.assertIn('period_months', response.data)

    def test_projection_endpoint_upper_bound_and_missing_required_fields(self):
        """Testa limites superiores (period_months > 600, monthly_contribution < 0) e campos obrigatórios."""
        payload = {
            "monthly_contribution": -50.0,
            "period_months": 601,
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('monthly_contribution', response.data)
        self.assertIn('annual_rate', response.data)
        self.assertIn('period_months', response.data)


class InvestmentSuggestionTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.User = get_user_model()
        self.client = APIClient()
        self.url = reverse('investment-suggestion')

    def test_generate_suggestion_conservative(self):
        from .services import generate_investment_suggestion
        result = generate_investment_suggestion(amount=10000.0, investor_profile='CONSERVATIVE')
        self.assertEqual(result['total_amount'], 10000.0)
        self.assertEqual(result['investor_profile'], 'CONSERVATIVE')

        total_allocated = sum(item['allocated_amount'] for item in result['allocations'])
        self.assertEqual(round(total_allocated, 2), 10000.0)

    def test_generate_suggestion_moderate(self):
        from .services import generate_investment_suggestion
        result = generate_investment_suggestion(amount=5000.0, investor_profile='MODERATE')
        total_allocated = sum(item['allocated_amount'] for item in result['allocations'])
        self.assertEqual(round(total_allocated, 2), 5000.0)
        self.assertEqual(result['investor_profile'], 'MODERATE')

    def test_generate_suggestion_aggressive(self):
        from .services import generate_investment_suggestion
        result = generate_investment_suggestion(amount=20000.0, investor_profile='AGGRESSIVE')
        total_allocated = sum(item['allocated_amount'] for item in result['allocations'])
        self.assertEqual(round(total_allocated, 2), 20000.0)
        self.assertEqual(result['investor_profile'], 'AGGRESSIVE')

    def test_endpoint_suggestion_with_existing_wallet_rebalances(self):
        from django.apps import apps
        from .models import Investment
        Wallet = apps.get_model('wallets', 'Wallet')
        WalletItem = apps.get_model('wallets', 'WalletItem')

        user = self.User.objects.create_user(
            username='rebalance_user',
            email='rebalance@example.com',
            password='secretpassword',
            investor_profile='MODERATE',
        )
        self.client.force_authenticate(user=user)

        # Cria investimento de Renda Fixa e adiciona R$ 10.000 na carteira do usuário
        rf_inv = Investment.objects.create(
            name="Tesouro Selic",
            type="FIXED_INCOME",
            risk_level="LOW",
            liquidity_deadline=0,
        )
        wallet, _ = Wallet.objects.get_or_create(user=user)
        WalletItem.objects.create(wallet=wallet, investment=rf_inv, amount=10000.0)

        # Novo aporte de R$ 5.000 para usuário Moderado (meta: 45% RF, 30% FII, 25% Ações)
        # Como o usuário já tem R$ 10.000 em Renda Fixa (66% do total projetado de R$ 15.000),
        # a renda fixa já está bem acima da meta (45% = R$ 6.750).
        # Logo, o novo aporte deve priorizar FII e Ações!
        payload = {"amount": 5000.0}
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['rebalanced'])
        self.assertEqual(response.data['current_portfolio_total'], 10000.0)

        allocations = {item['type']: item['allocated_amount'] for item in response.data['allocations']}
        # Renda fixa não deve receber novos recursos (ou quase zero), pois já está excedente
        self.assertEqual(allocations['FIXED_INCOME'], 0.0)
        # Todo o aporte deve ir para FII e STOCK
        self.assertGreater(allocations['FII'], 0.0)
        self.assertGreater(allocations['STOCK'], 0.0)
        self.assertEqual(round(allocations['FII'] + allocations['STOCK'], 2), 5000.0)

    def test_endpoint_suggestion_anonymous_with_profile(self):
        payload = {
            "amount": 10000.0,
            "investor_profile": "MODERATE",
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount'], 10000.0)
        self.assertEqual(response.data['investor_profile'], 'MODERATE')
        self.assertFalse(response.data['rebalanced'])
        self.assertTrue(len(response.data['allocations']) > 0)

    def test_endpoint_suggestion_authenticated_inherits_profile(self):
        user = self.User.objects.create_user(
            username='investor_user',
            email='investor@example.com',
            password='secretpassword',
            investor_profile='CONSERVATIVE',
        )
        self.client.force_authenticate(user=user)

        payload = {"amount": 5000.0}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['investor_profile'], 'CONSERVATIVE')

    def test_endpoint_missing_profile_returns_400(self):
        payload = {"amount": 5000.0}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_endpoint_invalid_amount_returns_400(self):
        payload = {"amount": 0.0, "investor_profile": "CONSERVATIVE"}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class InvestmentDetailAPITestCase(TestCase):
    def setUp(self):
        from .models import Investment
        self.client = APIClient()
        self.investment = Investment.objects.create(
            name="CDB Banco Master",
            type="FIXED_INCOME",
            risk_level="LOW",
            profitability=12.5,
            liquidity_deadline=30,
            description="CDB pré-fixado",
        )

    def test_get_investment_detail_success(self):
        response = self.client.get(f'/api/investments/{self.investment.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.investment.pk)
        self.assertEqual(response.data['name'], "CDB Banco Master")
        self.assertEqual(float(response.data['profitability']), 12.5)

    def test_get_investment_detail_not_found(self):
        response = self.client.get('/api/investments/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FinanceApiUnitTestCase(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_empty_or_none_ticker_returns_empty_dict(self, mock_sleep, mock_ticker):
        """Ticker vazio ou None deve retornar {} sem acionar sleep ou yfinance."""
        self.assertEqual(get_live_asset_data(''), {})
        self.assertEqual(get_live_asset_data(None), {})
        mock_sleep.assert_not_called()
        mock_ticker.assert_not_called()

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_get_live_asset_data_success_with_current_price(self, mock_sleep, mock_ticker):
        """Extrai currentPrice, converte dividendYield para porcentagem e armazena em cache."""
        mock_asset = MagicMock()
        mock_asset.info = {
            'currentPrice': 38.45,
            'dividendYield': 0.085,
            'currency': 'BRL',
            'longName': 'Petróleo Brasileiro S.A. - Petrobras',
            'sector': 'Energy',
        }
        mock_ticker.return_value = mock_asset

        result = get_live_asset_data('PETR4.SA')

        self.assertEqual(result, {
            'live_price': 38.45,
            'dividend_yield_percent': 8.5,
            'currency': 'BRL',
            'long_name': 'Petróleo Brasileiro S.A. - Petrobras',
            'sector': 'Energy',
        })
        mock_sleep.assert_called_once_with(0.3)
        mock_ticker.assert_called_once()
        self.assertEqual(cache.get('live_asset_data_PETR4.SA'), result)

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_get_live_asset_data_fallback_regular_market_price(self, mock_sleep, mock_ticker):
        """Quando currentPrice não está presente, deve usar regularMarketPrice."""
        mock_asset = MagicMock()
        mock_asset.info = {
            'regularMarketPrice': 10.25,
            'dividendYield': 0.12,
            'currency': 'BRL',
            'longName': 'Maxi Renda FII',
            'sector': 'Real Estate',
        }
        mock_ticker.return_value = mock_asset

        result = get_live_asset_data('MXRF11.SA')

        self.assertEqual(result['live_price'], 10.25)
        self.assertEqual(result['dividend_yield_percent'], 12.0)

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_get_live_asset_data_fallback_previous_close_and_defaults(self, mock_sleep, mock_ticker):
        """Usa previousClose como último fallback, mantém dividendYield None e currency padrão BRL."""
        mock_asset = MagicMock()
        mock_asset.info = {
            'previousClose': 125.0,
            'dividendYield': None,
        }
        mock_ticker.return_value = mock_asset

        result = get_live_asset_data('BOVA11.SA')

        self.assertEqual(result['live_price'], 125.0)
        self.assertIsNone(result['dividend_yield_percent'])
        self.assertEqual(result['currency'], 'BRL')
        self.assertIsNone(result['long_name'])
        self.assertIsNone(result['sector'])

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_get_live_asset_data_returns_cached_value_on_repeat_call(self, mock_sleep, mock_ticker):
        """Segunda chamada para o mesmo ticker deve usar o cache sem chamar yfinance novamente."""
        mock_asset = MagicMock()
        mock_asset.info = {
            'currentPrice': 62.10,
            'dividendYield': 0.06,
            'currency': 'BRL',
            'longName': 'Vale S.A.',
            'sector': 'Basic Materials',
        }
        mock_ticker.return_value = mock_asset

        first = get_live_asset_data('VALE3.SA')
        second = get_live_asset_data('VALE3.SA')

        self.assertEqual(first, second)
        self.assertEqual(mock_ticker.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 1)

    @patch('apps.investments.finance_api.yf.Ticker')
    @patch('time.sleep')
    def test_get_live_asset_data_handles_external_exception(self, mock_sleep, mock_ticker):
        """Falha na API externa deve retornar {} silenciosamente sem salvar no cache."""
        mock_ticker.side_effect = RuntimeError('Yahoo Finance unavailable')

        result = get_live_asset_data('INVALID.SA')

        self.assertEqual(result, {})
        self.assertIsNone(cache.get('live_asset_data_INVALID.SA'))


class InvestmentModelAndSerializerTestCase(TestCase):
    def test_investment_str_with_and_without_ticker(self):
        """__str__ deve exibir o ticker quando existir ou o tipo quando não houver ticker."""
        stock = Investment.objects.create(
            name='Petrobras',
            ticker='PETR4.SA',
            type='STOCK',
            risk_level='HIGH',
            liquidity_deadline=2,
        )
        fixed_income = Investment.objects.create(
            name='Tesouro Selic 2029',
            ticker=None,
            type='FIXED_INCOME',
            risk_level='LOW',
            profitability=10.75,
            liquidity_deadline=0,
        )

        self.assertEqual(str(stock), 'Petrobras (PETR4.SA)')
        self.assertEqual(str(fixed_income), 'Tesouro Selic 2029 (FIXED_INCOME)')

    @patch('apps.investments.serializers.get_live_asset_data')
    def test_serializer_fetches_live_data_only_when_ticker_present(self, mock_live_data):
        """InvestmentSerializer deve consultar live_data apenas para ativos com ticker."""
        mock_live_data.return_value = {
            'live_price': 52.30,
            'dividend_yield_percent': 1.8,
            'currency': 'BRL',
            'long_name': 'WEG S.A.',
            'sector': 'Industrials',
        }

        stock = Investment.objects.create(
            name='WEG',
            ticker='WEGE3.SA',
            type='STOCK',
            risk_level='MEDIUM',
            liquidity_deadline=2,
            description='Ação industrial',
        )
        fixed_income = Investment.objects.create(
            name='LCI Banco Inter',
            ticker=None,
            type='FIXED_INCOME',
            risk_level='LOW',
            profitability=9.8,
            liquidity_deadline=90,
            description='Isento de IR',
        )

        stock_data = InvestmentSerializer(stock).data
        fixed_data = InvestmentSerializer(fixed_income).data

        mock_live_data.assert_called_once_with('WEGE3.SA')
        self.assertEqual(stock_data['live_data']['live_price'], 52.30)
        self.assertIsNone(fixed_data['live_data'])


class InvestmentCatalogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('investment-catalog')

    def test_catalog_endpoint_empty_list(self):
        """Quando não há investimentos cadastrados, retorna HTTP 200 e lista vazia."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    @patch('apps.investments.serializers.get_live_asset_data')
    def test_catalog_endpoint_returns_assets_with_and_without_live_data(self, mock_live_data):
        """Retorna todos os ativos do catálogo com live_data populado para tickers e None para renda fixa."""
        mock_live_data.return_value = {
            'live_price': 10.50,
            'dividend_yield_percent': 11.4,
            'currency': 'BRL',
            'long_name': 'Maxi Renda FII',
            'sector': 'Real Estate',
        }

        Investment.objects.create(
            name='Maxi Renda',
            ticker='MXRF11.SA',
            type='FII',
            risk_level='MEDIUM',
            liquidity_deadline=2,
            description='Fundo imobiliário de papel',
        )
        Investment.objects.create(
            name='Tesouro IPCA+',
            ticker=None,
            type='FIXED_INCOME',
            risk_level='LOW',
            profitability=6.5,
            liquidity_deadline=0,
            description='Título público indexado à inflação',
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        by_name = {item['name']: item for item in response.data}
        self.assertEqual(by_name['Maxi Renda']['live_data']['live_price'], 10.50)
        self.assertIsNone(by_name['Tesouro IPCA+']['live_data'])
        self.assertEqual(by_name['Tesouro IPCA+']['liquidity_deadline'], 0)
        mock_live_data.assert_called_once_with('MXRF11.SA')


class SeedInvestmentsCommandTestCase(TestCase):
    def test_seed_investments_creates_assets_and_is_idempotent(self):
        """Executa o comando seed_investments duas vezes e garante que não duplica ativos."""
        from io import StringIO
        from django.core.management import call_command

        out_first = StringIO()
        call_command('seed_investments', stdout=out_first)

        self.assertEqual(Investment.objects.count(), 10)
        self.assertIn('10 novos ativos', out_first.getvalue())

        out_second = StringIO()
        call_command('seed_investments', stdout=out_second)

        self.assertEqual(Investment.objects.count(), 10)
        self.assertIn('0 novos ativos', out_second.getvalue())

