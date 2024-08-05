from django.urls import path
from .views import AddToCartView, CartDetailView

app_name = 'cart'

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('', CartDetailView.as_view(), name='cart_detail'),
]