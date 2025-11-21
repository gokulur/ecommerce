from cart.models import Cart
from wishlist.models import Wishlist

 

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {"cart_count": cart.items.count()}
        except Cart.DoesNotExist:
            return {"cart_count": 0}
    return {"cart_count": 0}


 

def wishlist_count(request):
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            return {"wishlist_count": wishlist.products.count()}
        except Wishlist.DoesNotExist:
            return {"wishlist_count": 0}
    return {"wishlist_count": 0}

