from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, ShippingAddress
from products.models import Product


# -----------------------------
# CHECKOUT PAGE (GET)
# -----------------------------
@login_required
def checkout_page(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_page")

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, "checkout.html", {
        "cart": cart,
        "total": total
    })


# -----------------------------
# CHECKOUT ACTION (POST)
# -----------------------------
@login_required
def checkout_action(request):
    if request.method != "POST":
        return redirect("checkout_page")

    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_page")

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # Create order items
    for pid, item in cart.items():
        product = get_object_or_404(Product, id=int(pid))

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=item['price']
        )

        # Reduce product stock
        product.stock -= item['quantity']
        product.save()

    # Create shipping address
    ShippingAddress.objects.create(
        order=order,
        full_name=request.POST.get("full_name"),
        address_line=request.POST.get("address_line"),
        city=request.POST.get("city"),
        postal_code=request.POST.get("postal_code"),
        country=request.POST.get("country"),
        phone=request.POST.get("phone")
    )

    # Clear cart
    request.session["cart"] = {}

    messages.success(request, f"✅ Order #{order.id} placed successfully!")
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
