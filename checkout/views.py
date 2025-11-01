from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .models import ShippingAddress

# -----------------------------
# CHECKOUT PAGE (GET)
# -----------------------------
@login_required
def checkout_page(request):
    """Show checkout form for latest order (or cart summary)"""
    cart = request.session.get('cart', {})
    # if not cart:
    #     messages.error(request, "Your cart is empty!")
    #     return redirect('product_list')  # or cart page

    total = sum(item['price']*item['quantity'] for item in cart.values())
    return render(request, 'checkout.html', {'cart': cart, 'total': total})

# -----------------------------
# CHECKOUT ACTION (POST)
# -----------------------------
@login_required
def checkout_action(request):
    """Create order + shipping address"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Cart is empty!")
            return redirect('checkout_page')

        total_price = sum(item['price']*item['quantity'] for item in cart.values())
        order = Order.objects.create(user=request.user, total_price=total_price)

        for pid, item in cart.items():
            from products.models import Product
            product = get_object_or_404(Product, id=int(pid))
            from orders.models import OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        # Create ShippingAddress
        full_name = request.POST.get('full_name')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        phone = request.POST.get('phone')

        ShippingAddress.objects.create(
            order=order,
            full_name=full_name,
            address_line=address_line,
            city=city,
            postal_code=postal_code,
            country=country,
            phone=phone
        )

        # Clear cart
        request.session['cart'] = {}
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('order_detail_page', order_id=order.id)
