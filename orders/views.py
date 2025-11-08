from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product

# -----------------------------
# ORDER LIST
# -----------------------------
@login_required
def order_list_page(request):
    """GET: list all orders for the logged-in user"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

# -----------------------------
# ORDER DETAIL
# -----------------------------
@login_required
def order_detail_page(request, order_id):
    """GET: show single order detail"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# -----------------------------
# CREATE ORDER
# -----------------------------
@login_required
def create_order_page(request):
    """GET: show form to create order (cart review)"""
    cart = request.session.get('cart', {})
    total = sum(item['price']*item['quantity'] for item in cart.values())
    return render(request, 'create_order.html', {'cart': cart, 'total': total})

@login_required
def create_order_action(request):
    """POST: create order from cart"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('create_order_page')

        total_price = sum(item['price']*item['quantity'] for item in cart.values())
        order = Order.objects.create(user=request.user, total_price=total_price)

        for pid, item in cart.items():
            product = get_object_or_404(Product, id=int(pid))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear cart
        request.session['cart'] = {}
        messages.success(request, f"Order #{order.id} created successfully!")
        return redirect('order_detail_page', order_id=order.id)

# -----------------------------
# UPDATE ORDER STATUS (admin)
# -----------------------------
@login_required
def update_order_status_page(request, order_id):
    """GET: show form to change status (admin only)"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/update_order_status.html', {'order': order})

@login_required
def update_order_status_action(request, order_id):
    """POST: change order status"""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, f"Order #{order.id} status updated!")
        return redirect('order_detail_page', order_id=order.id)
