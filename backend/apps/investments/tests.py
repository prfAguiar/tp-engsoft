from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

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
        """Testa se a projeção funciona apenas com montante inicial e juros."""
        result = calculate_projection(
            initial_amount=1000.0,
            monthly_contribution=0.0,
            annual_rate=10.0,
            period_months=12,
        )

        # Com 10% ao ano, em 12 meses R$ 1000 vira exatamente R$ 1100
        self.assertEqual(round(result['final_balance'], 2), 1100.0)
        self.assertEqual(round(result['total_interest_earned'], 2), 100.0)


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

    def test_projection_endpoint_validation_error(self):
        """Testa se dados inválidos retornam HTTP 400 Bad Request."""
        payload = {
            "initial_amount": -100.0,  # Inválido (menor que 0)
            "annual_rate": 150.0,     # Inválido (maior que 100)
            "period_months": 0,       # Inválido (menor que 1)
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
        from apps.investments.models import Investment
        from apps.wallets.models import Wallet, WalletItem

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
