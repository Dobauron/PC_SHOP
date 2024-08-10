from django.test import TestCase
from shop.models import Product, Category
from ..models import Order, OrderItem
from user_account.models import Account


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.00
        )

        self.order = Order.objects.create(user=self.user)

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} by {self.user}")

    def test_get_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), self.order_item.get_cost())

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f"{self.order_item.quantity} x {self.product.name}")

    def test_order_item_get_cost(self):
        self.assertEqual(self.order_item.get_cost(), self.product.price * self.order_item.quantity)

    def test_order_has_items(self):
        self.assertIn(self.order_item, self.order.items.all())
