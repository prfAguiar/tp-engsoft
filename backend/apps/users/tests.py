from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .services import calculate_investor_profile

User = get_user_model()


class InvestorProfileServicesTestCase(APITestCase):
    def test_conservative_profile_calculation(self):
        # Pontuação mínima: 4 * 1 = 4 (<= 6 -> CONSERVATIVE)
        result = calculate_investor_profile([1, 1, 1, 1])
        self.assertEqual(result['profile'], 'CONSERVATIVE')
        self.assertEqual(result['total_score'], 4)

        # Limite superior de conservador: 6 pontos
        result_edge = calculate_investor_profile([1, 2, 2, 1])
        self.assertEqual(result_edge['profile'], 'CONSERVATIVE')
        self.assertEqual(result_edge['total_score'], 6)

    def test_moderate_profile_calculation(self):
        # 7 a 9 pontos -> MODERATE
        result_lower = calculate_investor_profile([2, 2, 2, 1])
        self.assertEqual(result_lower['profile'], 'MODERATE')
        self.assertEqual(result_lower['total_score'], 7)

        result_upper = calculate_investor_profile([3, 2, 2, 2])
        self.assertEqual(result_upper['profile'], 'MODERATE')
        self.assertEqual(result_upper['total_score'], 9)

    def test_aggressive_profile_calculation(self):
        # 10 a 12 pontos -> AGGRESSIVE
        result_lower = calculate_investor_profile([3, 3, 2, 2])
        self.assertEqual(result_lower['profile'], 'AGGRESSIVE')
        self.assertEqual(result_lower['total_score'], 10)

        result_max = calculate_investor_profile([3, 3, 3, 3])
        self.assertEqual(result_max['profile'], 'AGGRESSIVE')
        self.assertEqual(result_max['total_score'], 12)


class InvestorProfileEndpointsTestCase(APITestCase):
    def setUp(self):
        self.questions_url = reverse('investor-quiz-questions')
        self.evaluate_url = reverse('investor-quiz-evaluate')

    def test_get_quiz_questions(self):
        response = self.client.get(self.questions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 4)

    def test_evaluate_quiz_unauthenticated(self):
        payload = {
            'answers': [
                {'question_id': 'horizon', 'score': 1},
                {'question_id': 'reaction', 'score': 1},
                {'question_id': 'knowledge', 'score': 1},
                {'question_id': 'goal', 'score': 1},
            ]
        }
        response = self.client.post(self.evaluate_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile'], 'CONSERVATIVE')
        self.assertFalse(response.data['saved'])

    def test_evaluate_quiz_authenticated_updates_profile(self):
        user = User.objects.create_user(
            username='cauaneto',
            email='cauaneto@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(user=user)

        payload = {
            'answers': [
                {'question_id': 'horizon', 'score': 3},
                {'question_id': 'reaction', 'score': 3},
                {'question_id': 'knowledge', 'score': 3},
                {'question_id': 'goal', 'score': 3},
            ]
        }
        response = self.client.post(self.evaluate_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile'], 'AGGRESSIVE')
        self.assertTrue(response.data['saved'])

        user.refresh_from_db()
        self.assertEqual(user.investor_profile, 'AGGRESSIVE')

    def test_evaluate_quiz_validation_errors(self):
        # Menos respostas do que o necessário
        payload_missing = {
            'answers': [
                {'question_id': 'horizon', 'score': 1},
            ]
        }
        res = self.client.post(self.evaluate_url, payload_missing, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Pergunta repetida
        payload_duplicate = {
            'answers': [
                {'question_id': 'horizon', 'score': 1},
                {'question_id': 'horizon', 'score': 2},
                {'question_id': 'knowledge', 'score': 1},
                {'question_id': 'goal', 'score': 1},
            ]
        }
        res_dup = self.client.post(self.evaluate_url, payload_duplicate, format='json')
        self.assertEqual(res_dup.status_code, status.HTTP_400_BAD_REQUEST)
