from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthAndLogoutTestCase(APITestCase):
    def test_registration_success(self):
        payload = {
            'email': 'novo@investidor.com',
            'password': 'StrongPassword123!',
            'first_name': 'Investidor',
            'last_name': 'Exemplo',
        }
        res = self.client.post('/api/users/register/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='novo@investidor.com').exists())

    def test_registration_rejects_weak_password(self):
        payload = {
            'email': 'fraco@investidor.com',
            'password': '123',
        }
        res = self.client.post('/api/users/register/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', res.data)

    def test_logout_blacklists_refresh_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken

        user = User.objects.create_user(
            username='logoutuser',
            email='logout@test.com',
            password='StrongPassword123!',
        )
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        res = self.client.post('/api/users/logout/', {'refresh': str(refresh)}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Tentar usar o mesmo refresh token deve falhar
        refresh_res = self.client.post('/api/users/token/refresh/', {'refresh': str(refresh)}, format='json')
        self.assertEqual(refresh_res.status_code, status.HTTP_401_UNAUTHORIZED)

