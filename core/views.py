from django.shortcuts import render
from products.models import Product
import random
# Create your views here.
def home(request):
    product_ids = list(Product.objects.values_list('id', flat=True))
    random.shuffle(product_ids)
    selected_ids = product_ids[:8]
    products = Product.objects.filter(id__in=selected_ids)
    return render(request, 'base.html', {'products': products})


