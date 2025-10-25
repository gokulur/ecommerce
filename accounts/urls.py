from django.urls import path
from . import views

urlpatterns = [
    # REGISTER
    path('register/', views.register_page, name='register_page'),
    path('register/action/', views.register_action, name='register_action'),

    # LOGIN
    path('login/', views.login_page, name='login_page'),
    path('login/action/', views.login_action, name='login_action'),

    # LOGOUT
    path('logout/', views.logout_action, name='logout_action'),

    # PASSWORD CHANGE
    path('password-change/', views.password_change_page, name='password_change_page'),
    path('password-change/action/', views.password_change_action, name='password_change_action'),

    # PASSWORD RESET
    path('password-reset/', views.password_reset_page, name='password_reset_page'),
    path('password-reset/action/', views.password_reset_action, name='password_reset_action'),

    # PASSWORD RESET CONFIRM
    path('reset/<str:token>/', views.password_reset_confirm_page, name='password_reset_confirm_page'),
    path('reset/<str:token>/action/', views.password_reset_confirm_action, name='password_reset_confirm_action'),


 
 
  
 

]
