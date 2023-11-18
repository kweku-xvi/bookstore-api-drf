from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.create_user_view, name='register_user'),
    path('login/', views.login_user_view, name='login_user'),
    path('users/', views.retrieve_all_users_view, name='retrieve_all_users'),
    path('reset-password/', views.password_reset_view, name='reset_password_view'),
    path('password-reset-confirm/', views.password_reset_view, name='password_reset_confirm_view'),
]
