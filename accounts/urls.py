from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.password_change_view, name='password_change'),
    path('password_reset/', views.password_reset_request_view, name='password_reset'),
    path('reset/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
