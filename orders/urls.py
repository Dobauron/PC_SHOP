# orders/urls.py
from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("history/", views.OrderHistoryView.as_view(), name="order_history"),
]
