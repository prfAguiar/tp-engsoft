from unittest.mock import MagicMock, patch

from django.contrib import admin
from django.test import TestCase

from apps.wallets.admin import WalletAdmin, WalletItemAdmin, WalletItemInline
from apps.wallets.models import Wallet, WalletItem
from apps.wallets.signals import create_user_wallet, update_wallet_total_on_item_change


class WalletSignalsUnitTestCase(TestCase):
    @patch('apps.wallets.signals.Wallet.objects.create')
    def test_create_user_wallet_creates_when_created_is_true(self, mock_create):
        dummy_user = MagicMock()
        create_user_wallet(sender=object, instance=dummy_user, created=True)
        mock_create.assert_called_once_with(user=dummy_user)

    @patch('apps.wallets.signals.Wallet.objects.create')
    def test_create_user_wallet_skips_when_created_is_false(self, mock_create):
        dummy_user = MagicMock()
        create_user_wallet(sender=object, instance=dummy_user, created=False)
        mock_create.assert_not_called()

    def test_update_wallet_total_calls_recalculate_when_wallet_id_present(self):
        dummy_item = MagicMock()
        dummy_item.wallet_id = 42
        update_wallet_total_on_item_change(sender=WalletItem, instance=dummy_item)
        dummy_item.wallet.recalculate_total.assert_called_once_with()

    def test_update_wallet_total_skips_when_wallet_id_is_none(self):
        dummy_item = MagicMock()
        dummy_item.wallet_id = None
        update_wallet_total_on_item_change(sender=WalletItem, instance=dummy_item)
        dummy_item.wallet.recalculate_total.assert_not_called()


class WalletAdminUnitTestCase(TestCase):
    def test_wallet_and_wallet_item_registered_in_admin_with_inline(self):
        self.assertIn(Wallet, admin.site._registry)
        self.assertIn(WalletItem, admin.site._registry)

        wallet_admin = admin.site._registry[Wallet]
        item_admin = admin.site._registry[WalletItem]
        self.assertIsInstance(wallet_admin, WalletAdmin)
        self.assertIsInstance(item_admin, WalletItemAdmin)
        self.assertIn(WalletItemInline, wallet_admin.inlines)
        self.assertEqual(WalletItemInline.model, WalletItem)
