from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.tests.factories import (
    auth_headers,
    create_user,
    get_expired_access_token,
    get_tokens_for_user,
)
from apps.wallets.models import Wallet


class UserProfileAPIIntegrationTestCase(APITestCase):
    def setUp(self):
        self.profile_url = reverse('user_profile')
        self.user = create_user(
            email='owner@finless.com',
            first_name='Beatriz',
            last_name='Alves',
            investor_profile='CONSERVATIVE',
        )
        self.access, _ = get_tokens_for_user(self.user)

    def test_profile_unauthenticated_returns_401_for_all_methods(self):
        self.assertEqual(self.client.get(self.profile_url).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.patch(self.profile_url, {'first_name': 'X'}, format='json').status_code, 401)
        self.assertEqual(self.client.put(self.profile_url, {'first_name': 'X'}, format='json').status_code, 401)

    def test_profile_expired_tampered_or_wrong_scheme_token_returns_401(self):
        expired = get_expired_access_token(self.user)
        tampered = f'{self.access[:-4]}XXXX'
        for headers in [auth_headers(expired), auth_headers(tampered), {'HTTP_AUTHORIZATION': f'Token {self.access}'}]:
            with self.subTest(headers=headers):
                self.assertEqual(self.client.get(self.profile_url, **headers).status_code, 401)

    def test_profile_inactive_user_with_existing_token_returns_401(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        self.assertEqual(self.client.get(self.profile_url, **auth_headers(self.access)).status_code, 401)

    def test_profile_get_returns_authenticated_user_without_password(self):
        res = self.client.get(self.profile_url, **auth_headers(self.access))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'owner@finless.com')
        self.assertEqual(res.data['first_name'], 'Beatriz')
        self.assertEqual(res.data['investor_profile'], 'CONSERVATIVE')
        self.assertNotIn('password', res.data)

    def test_profile_patch_persists_and_does_not_duplicate_wallet(self):
        res = self.client.patch(
            self.profile_url,
            {'first_name': 'Bia', 'investor_profile': 'MODERATE'},
            format='json',
            **auth_headers(self.access),
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Bia')
        self.assertEqual(self.user.investor_profile, 'MODERATE')
        self.assertEqual(Wallet.objects.filter(user=self.user).count(), 1)

    def test_profile_put_preserves_readonly_email_and_id(self):
        original_id = self.user.id
        payload = {
            'id': 999,
            'email': 'changed@finless.com',
            'first_name': 'Nova',
            'last_name': 'Silva',
            'investor_profile': 'AGGRESSIVE',
        }
        res = self.client.put(self.profile_url, payload, format='json', **auth_headers(self.access))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.id, original_id)
        self.assertEqual(self.user.email, 'owner@finless.com')
        self.assertEqual(self.user.investor_profile, 'AGGRESSIVE')

    def test_profile_patch_invalid_investor_profile_returns_400(self):
        res = self.client.patch(
            self.profile_url, {'investor_profile': 'INVALID'}, format='json', **auth_headers(self.access)
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(self.user.investor_profile, 'CONSERVATIVE')

    def test_profile_strict_isolation_between_two_users(self):
        other = create_user(email='other@finless.com', first_name='Carlos', investor_profile='AGGRESSIVE')
        other_access, _ = get_tokens_for_user(other)
        self.client.patch(self.profile_url, {'first_name': 'Alterado'}, format='json', **auth_headers(self.access))
        other_res = self.client.get(self.profile_url, **auth_headers(other_access))
        self.assertEqual(other_res.data['email'], 'other@finless.com')
        self.assertEqual(other_res.data['first_name'], 'Carlos')

    def test_profile_disallowed_methods_return_405(self):
        self.assertEqual(self.client.post(self.profile_url, {}, format='json', **auth_headers(self.access)).status_code, 405)
        self.assertEqual(self.client.delete(self.profile_url, **auth_headers(self.access)).status_code, 405)
