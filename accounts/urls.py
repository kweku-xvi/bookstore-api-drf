from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.create_user_view, name='register_user'),
    path('login/', views.login_user_view, name='login_user'),
    path('users/', views.retrieve_all_users_view, name='retrieve_all_users')
]
