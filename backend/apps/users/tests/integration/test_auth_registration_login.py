from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.users.tests.factories import DEFAULT_PASSWORD, auth_headers, create_user
from apps.wallets.models import Wallet


class RegistrationBootstrapIntegrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_register_creates_user_and_triggers_automatic_wallet(self):
        payload = {
            'email': 'bootstrap@finless.com',
            'password': DEFAULT_PASSWORD,
            'first_name': 'Clara',
            'last_name': 'Nunes',
        }
        res = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)

        user = User.objects.get(email='bootstrap@finless.com')
        self.assertEqual(user.username, 'bootstrap@finless.com')
        self.assertTrue(user.check_password(DEFAULT_PASSWORD))
        self.assertEqual(Wallet.objects.get(user=user).total_amount, Decimal('0.00'))

    def test_register_duplicate_email_returns_400_without_extra_wallet(self):
        create_user(email='dup.reg@finless.com')
        payload = {'email': 'dup.reg@finless.com', 'password': DEFAULT_PASSWORD}
        res = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email='dup.reg@finless.com').count(), 1)
        self.assertEqual(Wallet.objects.count(), 1)

    def test_register_invalid_payload_returns_400_without_persisting(self):
        res = self.client.post(self.register_url, {'email': 'invalido'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_register_get_method_returns_405(self):
        self.assertEqual(self.client.get(self.register_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class JwtLoginIntegrationTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.profile_url = reverse('user_profile')
        self.user = create_user(email='login@finless.com', first_name='Rafael')

    def test_login_valid_credentials_returns_jwt_pair_and_authenticates(self):
        res = self.client.post(
            self.login_url, {'email': 'login@finless.com', 'password': DEFAULT_PASSWORD}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

        profile_res = self.client.get(self.profile_url, **auth_headers(res.data['access']))
        self.assertEqual(profile_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res.data['email'], 'login@finless.com')

    def test_login_wrong_password_returns_401(self):
        res = self.client.post(
            self.login_url, {'email': 'login@finless.com', 'password': 'WrongPassword@99'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_email_returns_401(self):
        res = self.client.post(
            self.login_url, {'email': 'ghost@finless.com', 'password': DEFAULT_PASSWORD}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_inactive_user_returns_401(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        res = self.client.post(
            self.login_url, {'email': 'login@finless.com', 'password': DEFAULT_PASSWORD}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields_or_username_key_returns_400(self):
        payloads = [{}, {'email': 'login@finless.com'}, {'username': 'login@finless.com', 'password': DEFAULT_PASSWORD}]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post(self.login_url, payload, format='json').status_code, 400)
