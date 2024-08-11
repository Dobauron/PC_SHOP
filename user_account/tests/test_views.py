from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order, OrderItem
from ..models import Account
from shop.models import Product, Category


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(
            email="testuser@example.com", password="testpassword1@"
        )
        self.register_url = reverse("account_signup")
        self.login_url = reverse("account_login")
        self.logout_url = reverse("account_logout")
        self.dashboard_url = reverse("account:dashboard")

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_register_view_post(self):
        response = self.client.post(
            self.register_url,
            {
                "email": "newuser@example.com",
                "password1": "Newpassword12#",
                "password2": "Newpassword12#",
                "username": "newuser",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)
        user = Account.objects.get(email="newuser@example.com")
        self.assertTrue(user.check_password("Newpassword12#"))

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_login_view_post(self):
        response = self.client.post(
            self.login_url,
            {"login": "testuser@example.com", "password": "testpassword1@"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account:dashboard"))
        self.assertTrue(self.client.session["_auth_user_id"])

    def test_login_view_post_invalid(self):
        response = self.client.post(
            self.login_url,
            {"login": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "The email address and/or password you specified are not correct."
        )

    def test_logout_view(self):
        self.client.login(email="testuser@example.com", password="testpassword1@")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_dashboard_view(self):
        self.client.login(email="testuser@example.com", password="testpassword1@")
        category = Category.objects.create(name="test category")
        product = Product.objects.create(
            category=category, name="Test Product", price=100
        )
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=order, product=product, price=product.price, quantity=1
        )
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard.html")
        self.assertIn("orders", response.context)
        self.assertEqual(response.context["orders"].count(), 1)

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")
