from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from products.models import Product
from orders.models import Order
from django.contrib.auth.models import User
from products.models import Collection
from django.utils.text import slugify

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users
    })


# --- Product Management ---
@login_required
@user_passes_test(admin_only)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
@user_passes_test(admin_only)
def product_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')

        Product.objects.create(name=name, description=description, price=price, image=image)
        messages.success(request, "Product added successfully!")
        return redirect('admin_product_list')

    return render(request, 'product_form.html')


@login_required
@user_passes_test(admin_only)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('admin_product_list')

    return render(request, 'product_form.html', {'product': product})


@login_required
@user_passes_test(admin_only)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('admin_product_list')


# --- Order Management ---
@login_required
@user_passes_test(admin_only)
def order_list(request):
    orders = Order.objects.all().select_related('user')
    return render(request, 'admin_order_list.html', {'orders': orders})


@login_required
@user_passes_test(admin_only)
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, f"Order #{order.id} updated to {status}")
        return redirect('admin_order_list')
    return render(request, 'adminpanel/order_update.html', {'order': order})



def collection_list(request):
    collections = Collection.objects.all().order_by('-created_at')
    return render(request, 'collection_lists.html', {'collections': collections})


def collection_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name:
            messages.error(request, "Name is required.")
            return redirect('collection_add')

        collection = Collection.objects.create(
            name=name,
            slug=slugify(name),
            description=description,
            image=image
        )
        messages.success(request, f"Collection '{name}' added successfully!")
        return redirect('collection_list')

    return render(request, 'collection_add.html')


def collection_edit(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'POST':
        collection.name = request.POST.get('name')
        collection.description = request.POST.get('description')
        if request.FILES.get('image'):
            collection.image = request.FILES.get('image')
        collection.slug = slugify(collection.name)
        collection.save()
        messages.success(request, f"Collection '{collection.name}' updated successfully!")
        return redirect('collection_list')

    return render(request, 'admin/collection_add.html', {'collection': collection})


def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    collection.delete()
    messages.success(request, "Collection deleted successfully.")
    return redirect('collection_list')

def admin_customers(request):
    customers = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_customers.html', {'customers': customers})