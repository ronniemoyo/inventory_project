from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return {'cart_item_count': cart.items.count()}
    return {'cart_item_count': 0}