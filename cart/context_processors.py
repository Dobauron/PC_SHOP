from cart.models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        return {'cart': cart}
    return {'cart': None}