from django.test import TestCase

from apps.users.models import User
from apps.users.serializers import UserRegistrationSerializer
from apps.users.tests.factories import DEFAULT_PASSWORD, create_user


class UserRegistrationSerializerUnitTestCase(TestCase):
    def test_valid_full_payload_creates_user_with_username_equal_email(self):
        payload = {
            'email': 'ana@finless.com',
            'password': DEFAULT_PASSWORD,
            'first_name': 'Ana',
            'last_name': 'Silva',
        }
        serializer = UserRegistrationSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'ana@finless.com')
        self.assertEqual(user.first_name, 'Ana')
        self.assertEqual(user.last_name, 'Silva')
        self.assertTrue(user.check_password(DEFAULT_PASSWORD))

    def test_valid_minimal_payload_defaults_names_to_empty_string(self):
        s = UserRegistrationSerializer(data={'email': 'min@finless.com', 'password': DEFAULT_PASSWORD})
        self.assertTrue(s.is_valid(), s.errors)
        user = s.save()
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_password_is_write_only_and_never_serialized(self):
        s = UserRegistrationSerializer(data={'email': 'wo@finless.com', 'password': DEFAULT_PASSWORD})
        self.assertTrue(s.is_valid(), s.errors)
        s.save()
        self.assertNotIn('password', s.data)

    def test_password_boundary_seven_chars_rejected_and_eight_chars_accepted(self):
        short_s = UserRegistrationSerializer(data={'email': 'bva7@finless.com', 'password': 'Abc@123'})
        self.assertFalse(short_s.is_valid())
        self.assertIn('password', short_s.errors)

        exact_s = UserRegistrationSerializer(data={'email': 'bva8@finless.com', 'password': 'Abc@1234'})
        self.assertTrue(exact_s.is_valid(), exact_s.errors)

    def test_password_numeric_common_and_empty_rejected(self):
        for bad_pwd in ['12345678', 'password123', '', '        ']:
            with self.subTest(password=bad_pwd):
                s = UserRegistrationSerializer(data={'email': 'bad@finless.com', 'password': bad_pwd})
                self.assertFalse(s.is_valid())
                self.assertIn('password', s.errors)

    def test_password_similar_to_email_or_first_name_rejected(self):
        s = UserRegistrationSerializer(
            data={'email': 'mariana@finless.com', 'first_name': 'Mariana', 'password': 'mariana.costa'}
        )
        self.assertFalse(s.is_valid())
        self.assertIn('password', s.errors)

    def test_invalid_and_duplicate_email_rejected(self):
        create_user(email='taken@finless.com')
        for bad_email in ['sem-arroba', '@dominio.com', 'a@', 'a b@c.com', 'taken@finless.com']:
            with self.subTest(email=bad_email):
                s = UserRegistrationSerializer(data={'email': bad_email, 'password': DEFAULT_PASSWORD})
                self.assertFalse(s.is_valid())
                self.assertIn('email', s.errors)

    def test_field_max_length_boundaries(self):
        valid_254 = f"{'a' * 242}@example.com"
        invalid_255 = f"{'a' * 243}@example.com"
        self.assertTrue(
            UserRegistrationSerializer(
                data={'email': valid_254, 'password': DEFAULT_PASSWORD, 'first_name': 'N' * 150}
            ).is_valid()
        )
        self.assertFalse(
            UserRegistrationSerializer(data={'email': invalid_255, 'password': DEFAULT_PASSWORD}).is_valid()
        )
        self.assertFalse(
            UserRegistrationSerializer(
                data={'email': 'len@finless.com', 'password': DEFAULT_PASSWORD, 'first_name': 'N' * 151}
            ).is_valid()
        )

    def test_privileged_extra_fields_ignored_on_registration(self):
        payload = {
            'email': 'priv@finless.com',
            'password': DEFAULT_PASSWORD,
            'is_staff': True,
            'is_superuser': True,
            'investor_profile': 'AGGRESSIVE',
        }
        s = UserRegistrationSerializer(data=payload)
        self.assertTrue(s.is_valid(), s.errors)
        user = s.save()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.investor_profile)
        self.assertEqual(User.objects.filter(email='priv@finless.com').count(), 1)
