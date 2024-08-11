from django import template


register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def cart_total(cart):
    if cart:
        return sum(item.quantity * item.product.price for item in cart.items.all())
    return 0
