from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from ..models import Order, OrderItem
from cart.models import Cart, CartItem
from user_account.models import Account
from shop.models import Product, Category


class OrderCreateViewTestCase(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.login(email="testuser@example.com", password="testpassword")

        # Set up URLs
        self.create_order_url = reverse("orders:order_create")

        # Create Category and Product
        self.category = Category.objects.create(
            name="Karta graficzna", slug="karta-graficzna"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="DDR 6",
            slug="ddr-6",
            price=Decimal("10.00"),
            available=True,
        )

        # Create Cart and CartItem
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=1
        )

    def test_order_create_view_post_valid(self):
        response = self.client.post(self.create_order_url, {})

        self.assertEqual(response.status_code, 302)

        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)

        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(OrderItem.objects.first().product, self.product)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_order_create_view_post_invalid(self):
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(CartItem.objects.count(), 1)
