from django.shortcuts import render, get_object_or_404
from .models import Product, Category , Collection
from django.core.paginator import Paginator
def all_collections(request):
    categories = Category.objects.all()

    # Annotate each category with count of available products only
    for category in categories:
        category.available_count = category.products.filter(available=True).count()

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
    collections = Collection.objects.filter(category=category)
    products = Product.objects.filter(category=category, available=True).order_by('-created_at')
    cat=Category.objects.all()
    return render(request, 'products_by_category.html', {
        'products': products, 
        'category': category,
        'collections': collections,
        'categories': cat
    })


def products_by_collection(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    return render(request, 'products_by_collection.html', {
        'collection': collection
    })