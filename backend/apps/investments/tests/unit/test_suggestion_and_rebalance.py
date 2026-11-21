from decimal import Decimal

from django.test import SimpleTestCase, TestCase

from apps.investments.models import Investment
from apps.investments.rebalance import calculate_rebalanced_allocation
from apps.investments.serializers import InvestmentSuggestionInputSerializer
from apps.investments.services import generate_investment_suggestion
from apps.investments.strategies import ALLOCATION_PROFILES
from apps.wallets.models import WalletItem
from apps.wallets.tests.factories import create_user_with_jwt


class PortfolioRebalanceUnitTestCase(SimpleTestCase):
    def test_rebalance_prioritizes_deficit_categories(self):
        target_weights = {
            'FIXED_INCOME': Decimal('0.45'),
            'FII': Decimal('0.30'),
            'STOCK': Decimal('0.25'),
        }
        current = {
            'FIXED_INCOME': Decimal('10000.00'),
            'FII': Decimal('0.00'),
            'STOCK': Decimal('0.00'),
        }
        breakdown = calculate_rebalanced_allocation(
            projected_total=Decimal('15000.00'),
            contribution_amount=Decimal('5000.00'),
            target_weights=target_weights,
            current_by_type=current,
        )
        self.assertEqual(breakdown['FIXED_INCOME'], Decimal('0.00'))
        self.assertGreater(breakdown['FII'], Decimal('0.00'))
        self.assertGreater(breakdown['STOCK'], Decimal('0.00'))
        self.assertEqual(sum(breakdown.values()), Decimal('5000.00'))

    def test_rebalance_without_deficit_falls_back_to_target_weights(self):
        target_weights = {
            'FIXED_INCOME': Decimal('0.50'),
            'FII': Decimal('0.30'),
            'STOCK': Decimal('0.20'),
        }
        # Todas as categorias já superam a meta projetada (total_deficit == 0)
        current = {
            'FIXED_INCOME': Decimal('10000.00'),
            'FII': Decimal('6000.00'),
            'STOCK': Decimal('4000.00'),
        }
        breakdown = calculate_rebalanced_allocation(
            projected_total=Decimal('1000.00'),
            contribution_amount=Decimal('1000.00'),
            target_weights=target_weights,
            current_by_type=current,
        )
        self.assertEqual(breakdown['FIXED_INCOME'], Decimal('500.00'))
        self.assertEqual(breakdown['FII'], Decimal('300.00'))
        self.assertEqual(breakdown['STOCK'], Decimal('200.00'))


class InvestmentSuggestionServiceUnitTestCase(TestCase):
    def test_allocation_profiles_weights_sum_to_100_percent(self):
        for profile, data in ALLOCATION_PROFILES.items():
            total_pct = sum(item['percentage'] for item in data['allocations'])
            self.assertEqual(total_pct, 100.0, f'{profile} does not sum to 100%')

    def test_unknown_investor_profile_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, 'não reconhecido'):
            generate_investment_suggestion(amount=1000.0, investor_profile='SPECULATIVE')

    def test_suggestion_input_serializer_bounds_and_optional_profile(self):
        self.assertTrue(InvestmentSuggestionInputSerializer(data={'amount': 100.0}).is_valid())
        self.assertFalse(InvestmentSuggestionInputSerializer(data={'amount': 0.5}).is_valid())
        self.assertFalse(
            InvestmentSuggestionInputSerializer(
                data={'amount': 100.0, 'investor_profile': 'INVALID'}
            ).is_valid()
        )

    def test_suggestion_handles_unmapped_wallet_asset_type_and_catalog_assets(self):
        user, _, _ = create_user_with_jwt(email='unit.suggest@finless.com')
        crypto = Investment.objects.create(
            name='Bitcoin ETF',
            ticker='HASH11.SA',
            type='CRYPTO',
            risk_level='HIGH',
            liquidity_deadline=2,
        )
        WalletItem.objects.create(wallet=user.wallet, investment=crypto, amount=Decimal('1000.00'))

        result = generate_investment_suggestion(
            amount=2000.0,
            investor_profile='MODERATE',
            wallet=user.wallet,
        )
        self.assertTrue(result['rebalanced'])
        self.assertEqual(result['current_portfolio_total'], 1000.0)
