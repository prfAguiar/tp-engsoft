from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.tests.factories import auth_headers, create_user, get_tokens_for_user


class SuitabilityQuizAPIIntegrationTestCase(APITestCase):
    def setUp(self):
        self.questions_url = reverse('investor-quiz-questions')
        self.evaluate_url = reverse('investor-quiz-evaluate')

    def test_get_quiz_questions_returns_four_structured_questions(self):
        response = self.client.get(self.questions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 4)

    def test_evaluate_quiz_unauthenticated_computes_profile_without_saving(self):
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
        self.assertEqual(response.data['total_score'], 4)
        self.assertFalse(response.data['saved'])

    def test_evaluate_quiz_authenticated_persists_profile_on_user(self):
        user = create_user(email='quiz.investor@finless.com', investor_profile='CONSERVATIVE')
        access, _ = get_tokens_for_user(user)

        payload = {
            'answers': [
                {'question_id': 'horizon', 'score': 3},
                {'question_id': 'reaction', 'score': 3},
                {'question_id': 'knowledge', 'score': 3},
                {'question_id': 'goal', 'score': 3},
            ]
        }
        response = self.client.post(
            self.evaluate_url,
            payload,
            format='json',
            **auth_headers(access),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile'], 'AGGRESSIVE')
        self.assertTrue(response.data['saved'])

        user.refresh_from_db()
        self.assertEqual(user.investor_profile, 'AGGRESSIVE')

    def test_evaluate_quiz_rejects_incomplete_or_duplicate_answers(self):
        missing = {'answers': [{'question_id': 'horizon', 'score': 1}]}
        res_missing = self.client.post(self.evaluate_url, missing, format='json')
        self.assertEqual(res_missing.status_code, status.HTTP_400_BAD_REQUEST)

        duplicate = {
            'answers': [
                {'question_id': 'horizon', 'score': 1},
                {'question_id': 'horizon', 'score': 2},
                {'question_id': 'knowledge', 'score': 1},
                {'question_id': 'goal', 'score': 1},
            ]
        }
        res_dup = self.client.post(self.evaluate_url, duplicate, format='json')
        self.assertEqual(res_dup.status_code, status.HTTP_400_BAD_REQUEST)
