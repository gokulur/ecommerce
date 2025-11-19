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
    cart = Cart.objects.get(user=request.user) 
    collections = Collection.objects.all()[:6]

    return render(request, 'base.html', {
        'products': products,
        'collections': collections,
        'cart': cart
    })
