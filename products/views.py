from django.shortcuts import render, get_object_or_404
from .models import Product, Category 
from django.core.paginator import Paginator
def all_collections(request):
    categories = Category.objects.all()
    return render(request, 'all_collections.html', {'categories': categories})



def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {'page_obj': page_obj})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'product_detail.html', {'product': product})

def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True).order_by('-created_at')
    return render(request, 'products_by_category.html', {
        'products': products, 
        'category': category
    })