from django.shortcuts import render
from products.models import Product, Collection
from cart.models import Cart
import random

def home(request):
    product_ids = list(Product.objects.values_list('id', flat=True))
    random.shuffle(product_ids)
    selected_ids = product_ids[:8]

    # preserve order
    products = list(Product.objects.filter(id__in=selected_ids))
    products.sort(key=lambda p: selected_ids.index(p.id))
    
    # Get cart for logged in users
    cart = None
    recommended_products = []
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get recommended products (excluding cart items)
        cart_product_ids = cart.items.values_list('product_id', flat=True)
        recommended_products = list(Product.objects.exclude(id__in=cart_product_ids).filter(available=True)[:8])
        random.shuffle(recommended_products)
        recommended_products = recommended_products[:4]
    
    collections = Collection.objects.all()[:6]

    return render(request, 'base.html', {
        'products': products,
        'collections': collections,
        'cart': cart,
        'recommended_products': recommended_products
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')