from django.shortcuts import get_object_or_404, redirect,render
from .models import Cart, CartItem
from products.models import Product

# -------------------------------
# GET CART
# -------------------------------
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # If anonymous user → store cart in session
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
    return cart


# -------------------------------
# ADD TO CART
# -------------------------------

def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
    item.save()

    return redirect("cart_page")




# -------------------------------
# VIEW CART
# -------------------------------
def cart_page(request):
    cart = get_cart(request)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "cart.html", {
        "cart": cart,
        "items": items,
        "total": total,
    })


# -------------------------------
# INCREASE QUANTITY
# -------------------------------

def increase_qty(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect("cart_page")

# -------------------------------
# DECREASE QUANTITY
# -------------------------------
def decrease_qty(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # delete item if reaching 0

    return redirect("cart_page")


# -------------------------------
# REMOVE ITEM
# -------------------------------
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart_page")


# -------------------------------
#  CLEAR CART
# -------------------------------
def clear_cart(request):
    cart = get_cart(request)
    cart.items.all().delete()
    return redirect("cart_page")

