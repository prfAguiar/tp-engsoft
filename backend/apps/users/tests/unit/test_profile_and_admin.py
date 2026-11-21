from django.contrib import admin
from django.test import TestCase

from apps.users.admin import CustomUserAdmin
from apps.users.models import User
from apps.users.serializers import UserProfileSerializer
from apps.users.tests.factories import create_user


class UserProfileSerializerUnitTestCase(TestCase):
    def setUp(self):
        self.user = create_user(
            email='perfil@finless.com',
            first_name='Lucas',
            last_name='Mendes',
            investor_profile='MODERATE',
        )

    def test_serializes_expected_fields_and_omits_sensitive_data(self):
        data = UserProfileSerializer(self.user).data
        self.assertEqual(
            set(data.keys()),
            {'id', 'email', 'first_name', 'last_name', 'investor_profile'},
        )
        self.assertNotIn('password', data)
        self.assertNotIn('is_superuser', data)
        self.assertEqual(data['email'], 'perfil@finless.com')
        self.assertEqual(data['investor_profile'], 'MODERATE')

    def test_partial_update_persists_unicode_names_and_profile(self):
        serializer = UserProfileSerializer(
            self.user,
            data={'first_name': 'João', 'last_name': 'Conceição', 'investor_profile': 'AGGRESSIVE'},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'João')
        self.assertEqual(self.user.last_name, 'Conceição')
        self.assertEqual(self.user.investor_profile, 'AGGRESSIVE')

    def test_read_only_fields_id_and_email_cannot_be_overwritten(self):
        original_id = self.user.id
        serializer = UserProfileSerializer(
            self.user,
            data={'id': 99999, 'email': 'hacker@evil.com', 'first_name': 'Novo'},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.id, original_id)
        self.assertEqual(self.user.email, 'perfil@finless.com')
        self.assertEqual(self.user.first_name, 'Novo')

    def test_investor_profile_invalid_choice_rejected(self):
        for invalid in ['INVALID', 'moderate']:
            with self.subTest(investor_profile=invalid):
                serializer = UserProfileSerializer(
                    self.user,
                    data={'investor_profile': invalid},
                    partial=True,
                )
                self.assertFalse(serializer.is_valid())
                self.assertIn('investor_profile', serializer.errors)

    def test_investor_profile_can_be_cleared_to_none(self):
        serializer = UserProfileSerializer(
            self.user,
            data={'investor_profile': None},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.user.refresh_from_db()
        self.assertIsNone(self.user.investor_profile)


class CustomUserAdminUnitTestCase(TestCase):
    def test_user_registered_in_admin_with_investor_profile_fieldset(self):
        self.assertIn(User, admin.site._registry)
        model_admin = admin.site._registry[User]
        self.assertIsInstance(model_admin, CustomUserAdmin)
        self.assertIn('investor_profile', model_admin.list_display)
        self.assertIn('investor_profile', model_admin.list_filter)
        fieldset_titles = [title for title, _ in model_admin.fieldsets]
        self.assertIn('Perfil de Investimento', fieldset_titles)
