from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Cart, CartItem, Product


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
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
                request.session["cart_id"] = cart.id
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

    qty = int(request.POST.get("quantity", 1))
    
    if not created:
        item.quantity += qty  # Add to existing quantity
    else:
        item.quantity = qty  # Set initial quantity
    
    item.save()  # Save ONLY ONCE

    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = cart.items.all()
        total = sum(item.total_price for item in items)
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': sum(item.quantity for item in items),
            'cart_total': float(total)
        })
    
    return redirect("cart_page")


# -------------------------------
# VIEW CART
# -------------------------------
def cart_page(request):
    cart = get_cart(request)
    items = cart.items.all()
    total = sum(item.total_price for item in items)

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
    product = item.product

    # Check stock limit
    if item.quantity >= product.stock:
        return JsonResponse({
            'success': False,
            'limit_reached': True,
            'quantity': item.quantity,
            'item_total': float(item.total_price),
            'cart_total': float(sum(i.total_price for i in item.cart.items.all()))
        })
    
    # Increase by 1
    item.quantity += 1
    item.save()

    cart = item.cart
    items = cart.items.all()
    total = sum(i.total_price for i in items)

    # If from checkout page, redirect
    if "checkout" in request.GET:
        return redirect("checkout_page")

    return JsonResponse({
        'success': True,
        'quantity': item.quantity,
        'item_total': float(item.total_price),
        'cart_total': float(total),
    })


# -------------------------------
# DECREASE QUANTITY
# -------------------------------
def decrease_qty(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    cart = item.cart
 
    # Block if quantity is 1
    if item.quantity == 1:
        return JsonResponse({
            "success": False,
            "block": True,
            "quantity": item.quantity,
            "item_total": float(item.total_price),
            "cart_total": float(sum(i.total_price for i in cart.items.all()))
        })

    # Decrease by 1
    item.quantity -= 1
    item.save()

    total = sum(i.total_price for i in cart.items.all())

    # If from checkout page, redirect
    if "checkout" in request.GET:
        return redirect("checkout_page")

    return JsonResponse({
        "success": True,
        "block": False,
        "quantity": item.quantity,
        "item_total": float(item.total_price),
        "cart_total": float(total)
    })


# -------------------------------
# REMOVE ITEM
# -------------------------------
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    cart = item.cart
    item.delete()
    
    items = cart.items.all()
    total = sum(item.total_price for item in items)
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': float(total),
            'cart_count': sum(i.quantity for i in items)
        })
    
    return redirect("cart_page")