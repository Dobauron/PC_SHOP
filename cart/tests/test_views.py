from django.test import TestCase, Client
from django.urls import reverse
from ..models import Cart, CartItem
from shop.models import Product, Category
from decimal import Decimal
from user_account.models import Account


class CartViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.login(email="testuser@example.com", password="testpassword")

        # Create a category and product
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            slug="laptop",
            price=Decimal("999.99"),
            available=True,
        )

        # URL endpoints
        self.add_to_cart_url = reverse("cart:add_to_cart")
        self.cart_detail_url = reverse("cart:cart_detail")
        self.remove_from_cart_url = lambda item_id: reverse(
            "cart:remove_from_cart", args=[item_id]
        )

    def test_add_to_cart_view(self):
        # Post a valid form to add a product to the cart
        response = self.client.post(
            self.add_to_cart_url, {"product_id": self.product.id, "quantity": 2}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after adding
        self.assertRedirects(response, self.cart_detail_url)

        # Check if the cart item was created
        user_cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=user_cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_invalid_product(self):
        # Try adding a non-existing product
        response = self.client.post(
            self.add_to_cart_url, {"product_id": 999, "quantity": 2}
        )
        self.assertEqual(response.status_code, 404)  # Should return a 404 error

    def test_cart_detail_view(self):
        # Add a product to the cart first
        user_cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=1)

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart_detail.html")
        self.assertContains(response, self.product.name)

    def test_cart_detail_view_empty(self):
        # Ensure the view works even if the cart is empty
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart_detail.html")
        self.assertContains(
            response, "Your cart is empty"
        )  # Assuming the template includes this message

    def test_remove_from_cart_view(self):
        # Add a product to the cart first
        user_cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=user_cart, product=self.product, quantity=1
        )

        # Remove the product from the cart
        response = self.client.post(self.remove_from_cart_url(cart_item.id))
        self.assertEqual(response.status_code, 302)  # Should redirect after removing
        self.assertRedirects(response, self.cart_detail_url)

        # Check if the cart item was deleted
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(id=cart_item.id)

    def test_remove_nonexistent_cart_item(self):
        # Try to remove an item that doesn't exist
        response = self.client.post(self.remove_from_cart_url(999))
        self.assertEqual(response.status_code, 404)
