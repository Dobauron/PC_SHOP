from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Group, Permission
from ..forms import UserRegistrationForm, UserLoginForm

User = get_user_model()

class AccountViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.dashboard_url = reverse('accounts:dashboard')

        # Create a user for testing
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            username='testuser'
        )

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_register_view_post(self):
        response = self.client.post(self.register_url, {
            'email': 'newuser@example.com',
            'password1': 'Newpassword12#',
            'password2': 'Newpassword12#',
        })
        print(response.status_code)  # Should be 302
        print(response.context)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertRedirects(response, self.dashboard_url)
        self.assertEqual(str(self.client.session['_auth_user_id']), str(self.user.id))

    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
        self.assertIn('orders', response.context)
        self.assertEqual(response.context['orders'].count(), 0)  # Assuming no orders are created yet

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")
