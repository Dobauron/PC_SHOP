from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order, OrderItem
from ..forms import UserRegistrationForm, UserLoginForm
from ..models import Account
from shop.models import Product, Category


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(
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
        user = Account.objects.get(email='newuser@example.com')
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
        self.assertRedirects(response, reverse('accounts:dashboard'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Please enter a correct email address and password.'
                            ' Note that both fields may be case-sensitive.')

    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='test category')
        product = Product.objects.create(category=category,name='Test Product', price=100)
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=product, price=product.price, quantity=1)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
        self.assertIn('orders', response.context)
        self.assertEqual(response.context['orders'].count(), 1)

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")
