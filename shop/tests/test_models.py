from django.test import TestCase
from ..models import Category, Product


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Electronics", slug="electronics")

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "Electronics")

    def test_category_fields(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Electronics", slug="electronics")
        cls.product = Product.objects.create(
            category=cls.category,
            name="Smartphone",
            slug="smartphone",
            price=299.99,
            description="A high-quality smartphone.",
            available=True,
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), "Smartphone")

    def test_product_fields(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.slug, "smartphone")
        self.assertEqual(self.product.price, 299.99)
        self.assertEqual(self.product.description, "A high-quality smartphone.")
        self.assertTrue(self.product.available)

    def test_product_creation_without_image(self):
        product_without_image = Product.objects.create(
            category=self.category,
            name="Headphones",
            slug="headphones",
            price=99.99,
            description="High-quality headphones.",
            available=True,
        )
        self.assertEqual(str(product_without_image.image), "")
        self.assertIsNone(product_without_image.image.name)


class ProductCategoryIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Electronics", slug="electronics")
        cls.product = Product.objects.create(
            category=cls.category,
            name="Smartphone",
            slug="smartphone",
            price=299.99,
            description="A high-quality smartphone.",
            available=True,
        )

    def test_product_belongs_to_category(self):
        self.assertEqual(self.product.category.name, "Electronics")

    def test_category_products(self):
        products = self.category.products.all()
        self.assertIn(self.product, products)
