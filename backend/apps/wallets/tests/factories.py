from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from apps.investments.models import Investment
from apps.wallets.models import WalletItem

User = get_user_model()

DEFAULT_PASSWORD = 'K9#mP2!xQ7vL'


def create_user_with_jwt(
    email='wallet.user@finless.com',
    password=DEFAULT_PASSWORD,
    **extra_fields,
):
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        **extra_fields,
    )
    refresh = RefreshToken.for_user(user)
    return user, str(refresh.access_token), str(refresh)


def auth_headers(access_token):
    return {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}


def create_investment(
    name='Tesouro Selic 2029',
    inv_type='FIXED_INCOME',
    risk_level='LOW',
    profitability=Decimal('10.50'),
    liquidity_deadline=1,
    ticker=None,
    **extra_fields,
):
    return Investment.objects.create(
        name=name,
        type=inv_type,
        risk_level=risk_level,
        profitability=profitability,
        liquidity_deadline=liquidity_deadline,
        ticker=ticker,
        **extra_fields,
    )


def create_wallet_item(wallet, investment, amount=Decimal('100.00')):
    return WalletItem.objects.create(wallet=wallet, investment=investment, amount=amount)
