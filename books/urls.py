from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_all_books_view, name='get_all_books'),
    path('filter', views.filter_books_by_genre_or_rating_view, name='filter_books_view'),
    path('search', views.search_books_view, name='search_books_view'),
    path('<uuid:author_id>/add', views.add_book_view, name='add_book'),
    path('<str:book_isbn>', views.retrieve_book_view, name='retrieve_specific_book'),
    path('<str:book_isbn>/update', views.update_book_details_view, name='update_book_details'),
    path('<str:book_isbn>/delete', views.delete_book_view, name='delete_book'),
]