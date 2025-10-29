from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.filter(available=True).order_by('-created_at')
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'product_detail.html', {'product': product})
