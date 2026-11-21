from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.wallets.models import Wallet, WalletItem
from apps.wallets.tests.factories import (
    create_investment,
    create_user_with_jwt,
    create_wallet_item,
)


class WalletAndWalletItemModelUnitTestCase(TestCase):
    def setUp(self):
        self.user, _, _ = create_user_with_jwt(email='model@finless.com')
        self.wallet = Wallet.objects.get(user=self.user)
        self.investment = create_investment(name='Tesouro IPCA+', profitability=Decimal('6.25'))

    def test_wallet_str_and_default_fields(self):
        self.assertEqual(str(self.wallet), 'Wallet of model@finless.com')
        self.assertEqual(self.wallet.total_amount, Decimal('0.00'))
        self.assertIsNotNone(self.wallet.created_at)
        self.assertIsNotNone(self.wallet.updated_at)

    def test_wallet_item_str_representation(self):
        item = create_wallet_item(self.wallet, self.investment, amount=Decimal('250.50'))
        self.assertEqual(str(item), '250.50 in Tesouro IPCA+ (Wallet: model@finless.com)')

    def test_wallet_one_to_one_constraint_prevents_duplicate_wallet(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Wallet.objects.create(user=self.user)

    def test_wallet_item_unique_constraint_prevents_duplicate_asset_in_wallet(self):
        create_wallet_item(self.wallet, self.investment, amount=Decimal('100.00'))
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                create_wallet_item(self.wallet, self.investment, amount=Decimal('50.00'))

    def test_wallet_item_amount_min_value_boundary_validation(self):
        for invalid_amount in [Decimal('-0.01'), Decimal('0.00')]:
            with self.subTest(amount=invalid_amount):
                item = WalletItem(wallet=self.wallet, investment=self.investment, amount=invalid_amount)
                with self.assertRaises(ValidationError) as ctx:
                    item.full_clean()
                self.assertIn('amount', ctx.exception.message_dict)

        valid_min = WalletItem(wallet=self.wallet, investment=self.investment, amount=Decimal('0.01'))
        valid_min.full_clean()

    def test_recalculate_total_empty_wallet_resets_to_zero(self):
        Wallet.objects.filter(pk=self.wallet.pk).update(total_amount=Decimal('999.99'))
        self.wallet.refresh_from_db()
        result = self.wallet.recalculate_total()
        self.wallet.refresh_from_db()
        self.assertEqual(result, 0.00)
        self.assertEqual(self.wallet.total_amount, Decimal('0.00'))

    def test_recalculate_total_preserves_decimal_precision_without_float_drift(self):
        inv2 = create_investment(name='Ativo B', inv_type='STOCK', profitability=None)
        inv3 = create_investment(name='Ativo C', inv_type='FII', profitability=None)
        create_wallet_item(self.wallet, self.investment, amount=Decimal('0.10'))
        create_wallet_item(self.wallet, inv2, amount=Decimal('0.20'))
        create_wallet_item(self.wallet, inv3, amount=Decimal('0.01'))

        total = self.wallet.recalculate_total()
        self.wallet.refresh_from_db()
        self.assertEqual(total, Decimal('0.31'))
        self.assertEqual(self.wallet.total_amount, Decimal('0.31'))

    def test_recalculate_total_supports_max_15_digit_boundary(self):
        max_val = Decimal('9999999999999.99')
        create_wallet_item(self.wallet, self.investment, amount=max_val)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.total_amount, max_val)
