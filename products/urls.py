from django.urls import path
from . import views

urlpatterns = [
    path('', views.collection_list, name='collection_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
