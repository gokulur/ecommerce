from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_collections, name='all_collections'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.products_by_category, name='product_by_category'),
]
