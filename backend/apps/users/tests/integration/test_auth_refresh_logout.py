from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from apps.users.tests.factories import (
    DEFAULT_PASSWORD,
    auth_headers,
    create_user,
    get_expired_refresh_token,
    get_tokens_for_user,
)


class TokenRefreshAndLogoutIntegrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('user_profile')
        self.user = create_user(email='tokens@finless.com')
        self.access, self.refresh = get_tokens_for_user(self.user)

    def test_refresh_rotates_token_and_blacklists_previous_refresh(self):
        res = self.client.post(self.refresh_url, {'refresh': self.refresh}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertNotEqual(res.data['refresh'], self.refresh)

        reuse = self.client.post(self.refresh_url, {'refresh': self.refresh}, format='json')
        self.assertEqual(reuse.status_code, status.HTTP_401_UNAUTHORIZED)

        chained = self.client.post(self.refresh_url, {'refresh': res.data['refresh']}, format='json')
        self.assertEqual(chained.status_code, status.HTTP_200_OK)

    def test_refresh_rejects_access_token_malformed_expired_and_missing(self):
        expired = get_expired_refresh_token(self.user)
        for bad_token in [self.access, 'not.a.valid.jwt', expired]:
            with self.subTest(token=bad_token[:12]):
                res = self.client.post(self.refresh_url, {'refresh': bad_token}, format='json')
                self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.post(self.refresh_url, {}, format='json').status_code, 400)

    def test_logout_requires_authentication(self):
        res = self.client.post(self.logout_url, {'refresh': self.refresh}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_missing_or_empty_refresh_returns_400(self):
        for payload in [{}, {'refresh': ''}]:
            with self.subTest(payload=payload):
                res = self.client.post(self.logout_url, payload, format='json', **auth_headers(self.access))
                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('error', res.data)

    def test_logout_malformed_or_expired_refresh_returns_400(self):
        expired = get_expired_refresh_token(self.user)
        for bad_refresh in ['invalid-token', expired]:
            with self.subTest(refresh=bad_refresh[:12]):
                res = self.client.post(
                    self.logout_url, {'refresh': bad_refresh}, format='json', **auth_headers(self.access)
                )
                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('error', res.data)

    def test_logout_twice_with_same_refresh_returns_400_on_second_attempt(self):
        first = self.client.post(
            self.logout_url, {'refresh': self.refresh}, format='json', **auth_headers(self.access)
        )
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(BlacklistedToken.objects.count(), 1)
        second = self.client.post(
            self.logout_url, {'refresh': self.refresh}, format='json', **auth_headers(self.access)
        )
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_with_another_users_refresh_returns_403_without_blacklisting(self):
        other_user = create_user(email='victim@finless.com')
        _, victim_refresh = get_tokens_for_user(other_user)
        res = self.client.post(
            self.logout_url, {'refresh': victim_refresh}, format='json', **auth_headers(self.access)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BlacklistedToken.objects.count(), 0)

    def test_full_auth_lifecycle_register_login_refresh_logout(self):
        creds = {'email': 'cycle@finless.com', 'password': DEFAULT_PASSWORD}
        self.assertEqual(self.client.post(self.register_url, creds, format='json').status_code, 201)
        login_res = self.client.post(self.login_url, creds, format='json')
        ref_res = self.client.post(self.refresh_url, {'refresh': login_res.data['refresh']}, format='json')
        self.assertEqual(self.client.get(self.profile_url, **auth_headers(ref_res.data['access'])).status_code, 200)
        logout_res = self.client.post(
            self.logout_url, {'refresh': ref_res.data['refresh']}, format='json', **auth_headers(ref_res.data['access'])
        )
        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.post(self.refresh_url, {'refresh': ref_res.data['refresh']}, format='json').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
