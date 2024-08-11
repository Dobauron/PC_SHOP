from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone


class AccountManagerTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(email='user@example.com', password='password')
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(email='superuser@example.com', password='password')
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertTrue(superuser.check_password('password'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='superuser@example.com', password='password', is_staff=False)

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='superuser@example.com', password='password', is_superuser=False)


class AccountModelTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_user_creation(self):
        user = self.User.objects.create_user(email='user@example.com', password='password')
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertIsNotNone(user.created_at)
        self.assertIsInstance(user.created_at, timezone.datetime)

    def test_user_str_method(self):
        user = self.User.objects.create_user(email='user@example.com', password='password')
        self.assertEqual(str(user), 'user@example.com')
