from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout_page, name="checkout_page"),
    path("checkout/submit/", views.checkout_action, name="checkout_action"),
    path("order/<int:order_id>/", views.order_detail_page, name="order_detail_page"),
]
