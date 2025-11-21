from django.shortcuts import render
from products.models import Product, Collection
from cart.models import Cart
import random

def home(request):
    product_ids = list(Product.objects.values_list('id', flat=True))
    random.shuffle(product_ids)
    selected_ids = product_ids[:8]

    products = list(Product.objects.filter(id__in=selected_ids))
    products.sort(key=lambda p: selected_ids.index(p.id))

    recommended_products = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_product_ids = cart.items.values_list('product_id', flat=True)
            recommended_products = list(
                Product.objects.exclude(id__in=cart_product_ids)
                .filter(available=True)[:8]
            )
            random.shuffle(recommended_products)
            recommended_products = recommended_products[:4]

    collections = Collection.objects.all()[:6]

    return render(request, 'base.html', {
        'products': products,
        'collections': collections,
        'recommended_products': recommended_products
    })



def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')