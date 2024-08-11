from django.test import TestCase
from django.urls import reverse
from ..models import Product, Category


class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

        number_of_products = 15
        for i in range(number_of_products):
            Product.objects.create(
                category=cls.category,
                name=f"Product {i}",
                slug=f"product-{i}",
                price=10.00 + i,
                available=True,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertTemplateUsed(response, "shop/list.html")

    def test_view_context_contains_products(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertIn("products", response.context)
        self.assertEqual(
            len(response.context["products"]), 10
        )  # Oczekiwana liczba produktów na stronie

    def test_view_pagination(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["products"]), 10)

    def test_view_pagination_second_page(self):
        response = self.client.get(reverse("shop:product_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["products"]), 5
        )  # Pozostałe produkty na drugiej stronie

    def test_filter_by_category(self):
        response = self.client.get(
            reverse("shop:product_list_by_category", args=["test-category"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(
                product.category == self.category
                for product in response.context["products"]
            )
        )

    def test_context_contains_categories(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertIn("categories", response.context)
        self.assertEqual(
            response.context["categories"].count(), 1
        )  # Sprawdzenie liczby kategorii w kontekście

    def test_context_contains_selected_category(self):
        response = self.client.get(
            reverse("shop:product_list_by_category", args=["test-category"])
        )
        self.assertIn("category", response.context)
        self.assertEqual(response.context["category"], self.category)


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

        cls.product = Product.objects.create(
            category=cls.category,
            name="Test Product",
            slug="test-product",
            price=19.99,
            available=True,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(
            reverse("shop:product_detail", args=[self.product.pk, self.product.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("shop:product_detail", args=[self.product.pk, self.product.slug])
        )
        self.assertTemplateUsed(response, "shop/detail.html")

    def test_view_context_contains_product(self):
        response = self.client.get(
            reverse("shop:product_detail", args=[self.product.pk, self.product.slug])
        )
        self.assertIn("product", response.context)
        self.assertEqual(response.context["product"], self.product)
