from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from cart.models import CartItem
from .forms import OrderCreateForm


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "orders/order_create.html"

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        cart_items = CartItem.objects.filter(cart__user=self.request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )
        cart_items.delete()
        return redirect("orders:order_detail", pk=order.pk)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
