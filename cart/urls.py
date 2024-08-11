from django.urls import path
from .views import AddToCartView, CartDetailView, RemoveFromCartView

app_name = "cart"

urlpatterns = [
    path("add/", AddToCartView.as_view(), name="add_to_cart"),
    path("", CartDetailView.as_view(), name="cart_detail"),
    path(
        "remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove_from_cart"
    ),
]
