from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_books_in_the_cart, name='cart_items'),
    path('<uuid:book_isbn>/add/', views.add_book_to_cart, name='add_book_to_cart'),
    path('<uuid:book_isbn>/remove/', views.remove_book_from_cart, name='remove_book_from_cart'),
]