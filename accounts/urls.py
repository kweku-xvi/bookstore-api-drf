from . import views
from django.urls import path

urlpatterns = [
    path('register', views.create_user_view, name='register_user'),
    path('verify-user', views.verify_user_view, name='verify_user'),
    path('login', views.login_user_view, name='login_user'),
    path('users', views.retrieve_all_users_view, name='retrieve_users'),
    path('password-reset', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm', views.password_reset_confirm_view, name='password_reset_confirm'),
]
