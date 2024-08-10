from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order
from ..forms import UserRegistrationForm, UserLoginForm


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser'
        )
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.dashboard_url = reverse('accounts:dashboard')

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
            'username': 'newuser'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        user = self.User.objects.get(email='newuser@example.com')
        self.assertTrue(user.check_password('Newpassword12#'))

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:shop'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')
    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        Order.objects.create(user=self.user, product_name='Test Product', quantity=1)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
        self.assertIn('orders', response.context)
        self.assertEqual(response.context['orders'].count(), 1)


