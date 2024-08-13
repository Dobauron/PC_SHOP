from django import forms
from .models import Product

class ProductFilterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'price', 'brand']

    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
