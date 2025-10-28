from django.urls import path
from . import views  

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='admin_product_list'),
    path('products/add/', views.product_add, name='admin_product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='admin_product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='admin_product_delete'),
    path('orders/', views.order_list, name='admin_order_list'),
    path('orders/update/<int:pk>/', views.order_update_status, name='admin_order_update'),
    ]

