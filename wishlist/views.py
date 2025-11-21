from django.shortcuts import redirect, get_object_or_404,render
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Wishlist


@login_required
def wishlist_page(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, 'wishlist.html', {
        'products': products
    })

# @login_required
# def toggle_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     wishlist, created = Wishlist.objects.get_or_create(user=request.user)

#     if product in wishlist.products.all():
#         wishlist.products.remove(product)
#     else:
#         wishlist.products.add(product)
#     return redirect(request.META.get('HTTP_REFERER', '/'))

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
    else:
        wishlist.products.add(product)
        added = True

    return JsonResponse({
        "success": True,
        "added": added,
        "product_id": product_id
    })


