from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.users.models import User
from apps.users.tests.factories import DEFAULT_PASSWORD, create_superuser, create_user


class UserModelUnitTestCase(TestCase):
    def test_str_returns_user_email(self):
        user = create_user(email='str.user@finless.com')
        self.assertEqual(str(user), 'str.user@finless.com')

    def test_username_field_is_email_and_username_is_required(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertIn('username', User.REQUIRED_FIELDS)

    def test_create_user_hashes_password_and_sets_default_flags(self):
        user = create_user(email='hash@finless.com', password=DEFAULT_PASSWORD)
        self.assertNotEqual(user.password, DEFAULT_PASSWORD)
        self.assertTrue(user.check_password(DEFAULT_PASSWORD))
        self.assertFalse(user.check_password('SenhaErrada@99'))
        self.assertIsNone(user.investor_profile)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_sets_staff_and_superuser_flags(self):
        admin = create_superuser(email='root@finless.com')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password(DEFAULT_PASSWORD))

    def test_duplicate_email_raises_integrity_error(self):
        create_user(email='dup@finless.com', username='user_one')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                create_user(email='dup@finless.com', username='user_two')

    def test_duplicate_username_raises_integrity_error(self):
        create_user(email='first@finless.com', username='same_username')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                create_user(email='second@finless.com', username='same_username')

    def test_investor_profile_accepts_all_valid_choices_and_empty(self):
        valid_values = ['CONSERVATIVE', 'MODERATE', 'AGGRESSIVE', None, '']
        for idx, profile in enumerate(valid_values):
            with self.subTest(profile=profile):
                user = create_user(
                    email=f'choice{idx}@finless.com',
                    investor_profile=profile,
                )
                user.full_clean()
                self.assertEqual(user.investor_profile, profile)

    def test_investor_profile_rejects_invalid_choice_on_full_clean(self):
        user = create_user(email='invalid.choice@finless.com')
        user.investor_profile = 'ULTRA_AGGRESSIVE'
        with self.assertRaises(ValidationError) as ctx:
            user.full_clean()
        self.assertIn('investor_profile', ctx.exception.message_dict)
