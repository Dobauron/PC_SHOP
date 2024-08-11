from django.test import TestCase, Client
from ..models import Account
from django.urls import reverse
from ..forms import CustomSignupForm


class CustomSignupFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("account_signup")

    def test_valid_custom_signup_form(self):
        response = self.client.post(
            self.signup_url,
            {
                "email": "newuser@example.com",
                "username": "newuser",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)

        user = Account.objects.get(email="newuser@example.com")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("ComplexPass123!"))

    def test_invalid_custom_signup_form_mismatched_passwords(self):
        form = CustomSignupForm(
            data={
                "email": "newuser@example.com",
                "password1": "ComplexPass123!",
                "password2": "DifferentPass456!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_invalid_custom_signup_form_invalid_email(self):
        form = CustomSignupForm(
            data={
                "email": "invalidemail",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
