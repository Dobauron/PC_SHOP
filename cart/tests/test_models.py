from django.test import TestCase
from decimal import Decimal
from ..models import Cart, CartItem
from shop.models import Product, Category
from user_account.models import Account


class CartModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertIsNotNone(self.cart.created_at)

    def test_cart_str(self):
        self.assertEqual(
            str(self.cart),
            f"Cart for {self.user.email} created at {self.cart.created_at}",
        )


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=Decimal("10.00"),
            available=True,
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertIsNotNone(self.cart_item.added_at)

    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), "2 x Test Product")
