from django.urls import path
from . import views


urlpatterns = [
    path('<uuid:author_id>/add/', views.add_book_view, name='add_book'),
    path('<uuid:author_id>/all-books/', views.retrieve_books_by_author, name='retrieve_books_by_author'),
    path('<uuid:book_isbn>/', views.retrieve_book_view, name='retrieve_specific_book'),
    path('<uuid:book_isbn>/update/', views.update_book_details_view, name='update_book_details'),
    path('<uuid:book_isbn>/delete/', views.delete_book_view, name='delete_book'),
]