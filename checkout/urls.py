from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_page, name='checkout_page'),
    path('action/', views.checkout_action, name='checkout_action'),
]
