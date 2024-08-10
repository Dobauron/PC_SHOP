from django.test import TestCase, Client
from ..models import Account
from user_account.forms import UserRegistrationForm, UserLoginForm, CustomSignupForm
from django.urls import reverse


class UserRegistrationFormTest(TestCase):

    def test_valid_registration_form(self):
        form = UserRegistrationForm(data={
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form_mismatched_passwords(self):
        form = UserRegistrationForm(data={
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass456!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_registration_form_invalid_email(self):
        form = UserRegistrationForm(data={
            'email': 'invalidemail',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class UserLoginFormTest(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(email='testuser@example.com', password='testpassword')

    def test_valid_login_form(self):
        form = UserLoginForm(data={
            'username': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_wrong_email(self):
        form = UserLoginForm(data={
            'username': 'wronguser@example.com',
            'password': 'testpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_invalid_login_form_wrong_password(self):
        form = UserLoginForm(data={
            'username': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class CustomSignupFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:register')

    def test_valid_custom_signup_form(self):
        response = self.client.post(self.signup_url, {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })

        self.assertEqual(response.status_code, 302)

        user = Account.objects.get(email='newuser@example.com')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('ComplexPass123!'))

    def test_invalid_custom_signup_form_mismatched_passwords(self):
        form = CustomSignupForm(data={
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass456!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_custom_signup_form_invalid_email(self):
        form = CustomSignupForm(data={
            'email': 'invalidemail',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
