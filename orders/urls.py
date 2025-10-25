from django.urls import path
from . import views

urlpatterns = [
    # ORDER LIST & DETAIL
    path('', views.order_list_page, name='order_list_page'),
    path('<int:order_id>/', views.order_detail_page, name='order_detail_page'),

    # CREATE ORDER
    path('create/', views.create_order_page, name='create_order_page'),
    path('create/action/', views.create_order_action, name='create_order_action'),

    # UPDATE ORDER STATUS (admin)
    path('<int:order_id>/update/', views.update_order_status_page, name='update_order_status_page'),
    path('<int:order_id>/update/action/', views.update_order_status_action, name='update_order_status_action'),
]
