from django import forms
from shop.models import Product

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    product_id = forms.IntegerField(widget=forms.HiddenInput)