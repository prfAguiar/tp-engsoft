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
