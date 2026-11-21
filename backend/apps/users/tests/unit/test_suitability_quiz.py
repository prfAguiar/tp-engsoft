from django.test import SimpleTestCase

from apps.users.serializers import (
    InvestorProfileQuizAnswerSerializer,
    InvestorProfileQuizInputSerializer,
)
from apps.users.services import PROFILES, QUIZ_QUESTIONS, calculate_investor_profile


class SuitabilityQuizServiceUnitTestCase(SimpleTestCase):
    def test_quiz_questions_and_profiles_catalog_integrity(self):
        self.assertEqual(len(QUIZ_QUESTIONS), 4)
        expected_ids = ['horizon', 'reaction', 'knowledge', 'goal']
        self.assertEqual([q['id'] for q in QUIZ_QUESTIONS], expected_ids)
        for question in QUIZ_QUESTIONS:
            self.assertEqual([opt['value'] for opt in question['options']], [1, 2, 3])
        self.assertEqual(set(PROFILES.keys()), {'CONSERVATIVE', 'MODERATE', 'AGGRESSIVE'})

    def test_conservative_profile_boundary_values(self):
        for scores, expected_total in [([1, 1, 1, 1], 4), ([1, 2, 2, 1], 6)]:
            with self.subTest(total=expected_total):
                res = calculate_investor_profile(scores)
                self.assertEqual(res['profile'], 'CONSERVATIVE')
                self.assertEqual(res['profile_label'], 'Conservador')
                self.assertEqual(res['total_score'], expected_total)
                self.assertEqual((res['min_score'], res['max_score']), (4, 12))

    def test_moderate_profile_boundary_values(self):
        for scores, expected_total in [([2, 2, 2, 1], 7), ([3, 2, 2, 2], 9)]:
            with self.subTest(total=expected_total):
                res = calculate_investor_profile(scores)
                self.assertEqual(res['profile'], 'MODERATE')
                self.assertEqual(res['profile_label'], 'Moderado')
                self.assertEqual(res['total_score'], expected_total)

    def test_aggressive_profile_boundary_values(self):
        for scores, expected_total in [([3, 3, 2, 2], 10), ([3, 3, 3, 3], 12)]:
            with self.subTest(total=expected_total):
                res = calculate_investor_profile(scores)
                self.assertEqual(res['profile'], 'AGGRESSIVE')
                self.assertEqual(res['profile_label'], 'Agressivo')
                self.assertEqual(res['total_score'], expected_total)


class SuitabilityQuizSerializerUnitTestCase(SimpleTestCase):
    def test_answer_serializer_score_bounds(self):
        for valid_score in (1, 2, 3):
            s = InvestorProfileQuizAnswerSerializer(data={'question_id': 'goal', 'score': valid_score})
            self.assertTrue(s.is_valid())
        for invalid_score in (0, 4, -1):
            s = InvestorProfileQuizAnswerSerializer(data={'question_id': 'goal', 'score': invalid_score})
            self.assertFalse(s.is_valid())
            self.assertIn('score', s.errors)

    def test_input_serializer_valid_four_distinct_answers(self):
        payload = {
            'answers': [
                {'question_id': 'horizon', 'score': 1},
                {'question_id': 'reaction', 'score': 2},
                {'question_id': 'knowledge', 'score': 3},
                {'question_id': 'goal', 'score': 2},
            ]
        }
        serializer = InvestorProfileQuizInputSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_input_serializer_rejects_wrong_count_or_duplicate_question_ids(self):
        too_few = {'answers': [{'question_id': 'horizon', 'score': 1}]}
        self.assertFalse(InvestorProfileQuizInputSerializer(data=too_few).is_valid())

        duplicate = {
            'answers': [
                {'question_id': 'horizon', 'score': 1},
                {'question_id': 'horizon', 'score': 2},
                {'question_id': 'knowledge', 'score': 1},
                {'question_id': 'goal', 'score': 1},
            ]
        }
        serializer = InvestorProfileQuizInputSerializer(data=duplicate)
        self.assertFalse(serializer.is_valid())
        self.assertIn('answers', serializer.errors)
