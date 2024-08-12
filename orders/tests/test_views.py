from django.test import TestCase
from django.urls import reverse
from ..models import Order, OrderItem
from cart.models import CartItem, Cart
from decimal import Decimal
from user_account.models import Account
from shop.models import Product, Category


class OrderViewsTestCase(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.login(email="testuser@example.com", password="testpassword")
        self.create_order_url = reverse("orders:order_create")
        self.order_detail_url = lambda pk: reverse("orders:order_detail", args=[pk])
        self.order_history_url = reverse("orders:order_history")
        self.category = Category(name="Karta graficzna", slug="karta-graficzna")
        self.category.save()
        self.product = Product(
            category=self.category,
            name="DDR 6",
            slug="ddr-6",
            price=Decimal("10.00"),
            available=1,
        )
        self.product.save()
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=1
        )

    def test_order_create_view(self):
        response = self.client.post(
            self.create_order_url,
            {
                # Replace with actual form fields and values
                "field1": "value1",
                "field2": "value2",
            },
        )
        self.assertEqual(response.status_code, 302)  # Should redirect

        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(OrderItem.objects.first().product, self.product)
        self.assertEqual(CartItem.objects.count(), 0)  # Ensure cart items are deleted

    def test_order_detail_view(self):
        order = Order.objects.create(user=self.user)
        response = self.client.get(self.order_detail_url(order.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.id)
        self.assertContains(response, "Order Detail")

    def test_order_history_view(self):
        order1 = Order.objects.create(user=self.user)
        order2 = Order.objects.create(user=self.user)
        other_user = Account.objects.create_user(
            email="otheruser@example.com", password="otherpassword"
        )
        Order.objects.create(user=other_user)

        response = self.client.get(self.order_history_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order1.id)
        self.assertContains(response, order2.id)
        self.assertNotContains(response, "otheruser@example.com")
