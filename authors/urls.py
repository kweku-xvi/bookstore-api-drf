from django.urls import path
from . import views

urlpatterns = [
    path('filter', views.filter_authors_by_genre_view, name='filter_authors_view'),
    path('search', views.search_authors_by_name_or_genre_view, name='search_authors_view'),
    path('add', views.add_author_view, name='add_author'),
    path('all', views.retrieve_all_authors, name='retrieve_all_authors'),
    path('<uuid:author_id>', views.retrieve_author_view, name='retrieve_particular_author'),
    path('<uuid:author_id>/books', views.retrieve_books_by_author, name='retrieve_books_by_author'),
    path('<uuid:author_id>/update', views.update_author_view, name='update_author'),
    path('<uuid:author_id>/delete', views.delete_author_view, name='delete_author'),
]
