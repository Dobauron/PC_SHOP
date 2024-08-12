from django.test import TestCase
from ..forms import AddToCartForm


class AddToCartFormTest(TestCase):

    def test_form_valid_data(self):
        form = AddToCartForm(data={"product_id": 1, "quantity": 2})
        self.assertTrue(form.is_valid())

    def test_form_invalid_quantity(self):
        form = AddToCartForm(data={"product_id": 1, "quantity": 0})
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
        self.assertEqual(
            form.errors["quantity"],
            ["Ensure this value is greater than or equal to 1."],
        )

    def test_form_missing_product_id(self):
        form = AddToCartForm(data={"quantity": 2})
        self.assertFalse(form.is_valid())
        self.assertIn("product_id", form.errors)
        self.assertEqual(form.errors["product_id"], ["This field is required."])

    def test_form_initial_values(self):
        form = AddToCartForm()
        self.assertEqual(form.fields["quantity"].initial, 1)
        self.assertEqual(form.fields["quantity"].min_value, 1)
