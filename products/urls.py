from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('all_collections/', views.all_collections, name='all_collections'),

    path('category/<slug:slug>/', views.products_by_category, name='product_by_category'),

 
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
 
