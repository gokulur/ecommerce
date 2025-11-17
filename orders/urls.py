from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout_page, name="checkout_page"),
    path("checkout/submit/", views.checkout_action, name="checkout_action"),
    path("order/<int:order_id>/", views.order_detail_page, name="order_detail_page"),
    path("track/<int:order_id>/", views.track_order_page, name="track_order_page"),
    path("orders/", views.order_list_page, name="order_list_page"),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
]
