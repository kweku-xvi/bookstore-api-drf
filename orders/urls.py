from . import views
from django.urls import path

urlpatterns = [
    path('', views.ordering_all_books_in_a_cart, name='order_all_books'),
    path('<uuid:item_id>', views.ordering_a_particular_book, name='order_book'),
]