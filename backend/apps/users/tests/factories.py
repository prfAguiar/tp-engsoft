from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()

DEFAULT_PASSWORD = 'K9#mP2!xQ7vL'


def create_user(
    email='investor@finless.com',
    password=DEFAULT_PASSWORD,
    username=None,
    **extra_fields,
):
    return User.objects.create_user(
        username=username or email,
        email=email,
        password=password,
        **extra_fields,
    )


def create_superuser(
    email='admin@finless.com',
    password=DEFAULT_PASSWORD,
    username=None,
    **extra_fields,
):
    return User.objects.create_superuser(
        username=username or email,
        email=email,
        password=password,
        **extra_fields,
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def get_expired_access_token(user):
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=timedelta(seconds=-1))
    return str(token)


def get_expired_refresh_token(user):
    token = RefreshToken.for_user(user)
    token.set_exp(lifetime=timedelta(seconds=-1))
    return str(token)


def auth_headers(access_token):
    return {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
