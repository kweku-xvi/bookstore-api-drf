from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_books_in_the_cart, name='cart_items'),
    path('<uuid:cart_id>/', views.get_cart_item, name='get_cart_item'),
    path('<uuid:cart_id>/order/', views.order_particular_cart_item, name='order_particular_cart_item'),
    path('<uuid:book_isbn>/add/', views.add_book_to_cart, name='add_book_to_cart'),
    path('<uuid:cart_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('order/all/', views.order_all_items_in_cart, name='order_all_items_in_cart')
]