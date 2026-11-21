from decimal import Decimal

from django.test import TestCase

from apps.wallets.models import Wallet
from apps.wallets.serializers import WalletItemSerializer, WalletSerializer
from apps.wallets.tests.factories import (
    create_investment,
    create_user_with_jwt,
    create_wallet_item,
)


class WalletSerializersUnitTestCase(TestCase):
    def setUp(self):
        self.user, _, _ = create_user_with_jwt(email='ser@finless.com')
        self.wallet = Wallet.objects.get(user=self.user)

    def test_profitability_estimate_uses_explicit_positive_and_small_boundary(self):
        rf = create_investment(name='CDB 11.25', profitability=Decimal('11.25'))
        tiny = create_investment(name='Taxa Min', profitability=Decimal('0.01'))
        item_rf = create_wallet_item(self.wallet, rf, amount=Decimal('100.00'))
        item_tiny = create_wallet_item(self.wallet, tiny, amount=Decimal('100.00'))

        self.assertEqual(WalletItemSerializer(item_rf).data['profitability_estimate'], 11.25)
        self.assertEqual(WalletItemSerializer(item_tiny).data['profitability_estimate'], 0.01)

    def test_profitability_estimate_zero_explicit_does_not_fallback(self):
        zero_inv = create_investment(name='Ativo Zero', inv_type='STOCK', profitability=Decimal('0.00'))
        item = create_wallet_item(self.wallet, zero_inv, amount=Decimal('100.00'))
        self.assertEqual(WalletItemSerializer(item).data['profitability_estimate'], 0.0)

    def test_profitability_estimate_fallbacks_by_investment_type(self):
        stock = create_investment(name='PETR4', inv_type='STOCK', profitability=None)
        fii = create_investment(name='MXRF11', inv_type='FII', profitability=None)
        fixed = create_investment(name='RF Sem Taxa', inv_type='FIXED_INCOME', profitability=None)
        crypto = create_investment(name='BTC', inv_type='CRYPTO', profitability=None)

        cases = [(stock, 12.0), (fii, 9.0), (fixed, 10.5), (crypto, 10.5)]
        for inv, expected in cases:
            with self.subTest(inv_type=inv.type):
                item = create_wallet_item(self.wallet, inv, amount=Decimal('50.00'))
                self.assertEqual(WalletItemSerializer(item).data['profitability_estimate'], expected)

    def test_wallet_item_serializer_exposes_readonly_investment_metadata(self):
        inv = create_investment(name='WEG S.A.', inv_type='STOCK', profitability=None)
        item = create_wallet_item(self.wallet, inv, amount=Decimal('300.00'))
        data = WalletItemSerializer(item).data
        self.assertEqual(data['investment_name'], 'WEG S.A.')
        self.assertEqual(data['investment_type'], 'STOCK')
        self.assertEqual(data['amount'], '300.00')

    def test_wallet_item_serializer_amount_boundary_values(self):
        inv = create_investment(name='BVA Asset')
        for valid_amt in ['0.01', '9999999999999.99']:
            with self.subTest(valid_amount=valid_amt):
                s = WalletItemSerializer(data={'investment': inv.pk, 'amount': valid_amt})
                self.assertTrue(s.is_valid(), s.errors)

        invalid_amounts = ['-1.00', '-0.01', '0.00', '10000000000000.00', '10.123', 'abc']
        for bad_amt in invalid_amounts:
            with self.subTest(invalid_amount=bad_amt):
                s = WalletItemSerializer(data={'investment': inv.pk, 'amount': bad_amt})
                self.assertFalse(s.is_valid())
                self.assertIn('amount', s.errors)

    def test_wallet_serializer_nests_items_and_keeps_total_amount_readonly(self):
        inv = create_investment(name='Tesouro')
        create_wallet_item(self.wallet, inv, amount=Decimal('250.00'))
        self.wallet.refresh_from_db()

        serializer = WalletSerializer(self.wallet, data={'total_amount': '999999.00'}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, Decimal('250.00'))
        self.assertEqual(len(WalletSerializer(self.wallet).data['items']), 1)
