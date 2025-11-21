from cart.models import Cart
from wishlist.models import Wishlist

def cart_count(request):
    if request.user.is_authenticated:
        return {
            "cart_count": Cart.objects.filter(user=request.user).count()
        }
    return {"cart_count": 0}

def wishlist_count(request):
    if request.user.is_authenticated:
        return {
            "wishlist_count": Wishlist.objects.filter(user=request.user).count()
        }
    return {"wishlist_count": 0}
