from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, ShippingAddress
from products.models import Product
from cart.models import Cart, CartItem
from cart.views import get_cart

# -----------------------------
# CHECKOUT PAGE (GET)
# -----------------------------


@login_required
def checkout_page(request):
    cart = get_cart(request)
    items = cart.items.all()

    if not items:
        return redirect("cart_page")

    total = sum(i.total_price for i in items)

   
    profile = getattr(request.user, "profile", None)

    return render(request, "checkout.html", {
        "cart": cart,
        "items": items,
        "total": total,
        "profile": profile,
        "user": request.user,
    })




# -----------------------------
# CHECKOUT ACTION (POST)
# -----------------------------
@login_required
def checkout_action(request):
    cart = get_cart(request)
    items = cart.items.all()

    if not items:
        return redirect("cart_page")

    total_price = sum(i.total_price for i in items)

    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # create order items
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # shipping
    ShippingAddress.objects.create(
        order=order,
        full_name=request.POST.get('name'),
        address_line=request.POST.get('address_line'),
        city=request.POST.get('city'),
        postal_code=request.POST.get('postal_code'),
        country=request.POST.get('country'),
        phone=request.POST.get('phone'),
    )

    # clear cart
    cart.items.all().delete()
    messages.success(request, "🎉 Order placed successfully!")
    return redirect("order_detail_page", order_id=order.id)


# -----------------------------
# ORDER DETAIL PAGE
# -----------------------------
@login_required
def order_detail_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "order_detail.html", {
        "order": order,
        "items": order.items.all(),
        "shipping": order.shippingaddress
    })

# -----------------------------
# TRACK ORDER PAGE
# -----------------------------
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def track_order_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # order_status = order.status.lower()

    steps = {
        "processed": 1,
        "shipped": 2,
        "enroute": 3,
        "arrived": 4,
    }

    # active_step = steps.get(order_status, 1)

    return render(request, "track_order.html", {
        "order": order,
        # "active_step": active_step
    })


def order_list_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "order_list.html", {"orders": orders})

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    # check if item already exists
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": 1}
    )

    # if already in cart, set quantity = 1 (not increase)
    if not created:
        item.quantity = 1
        item.save()

    return redirect("checkout_page")
