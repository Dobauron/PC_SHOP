from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
from shop.models import Product
from .forms import AddToCartForm


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST or None)
        if form.is_valid():
            product_id = form.cleaned_data["product_id"]
            quantity = form.cleaned_data["quantity"]
            product = get_object_or_404(Product, id=product_id)

            user_cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, item_created = CartItem.objects.get_or_create(
                cart=user_cart, product=product
            )
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            return redirect("cart:cart_detail")
        return redirect("shop:product_list")


class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "cart/cart_detail.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        user_cart = Cart.objects.filter(user=self.request.user).first()
        if user_cart:
            return user_cart.items.all()
        return CartItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart.objects.filter(user=self.request.user).first()
        return context


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect("cart:cart_detail")
