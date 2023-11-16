from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:book_isbn>/add/', views.add_feedback_view, name='add_feedback'),
    path('<uuid:feedback_id>/', views.get_feedback_view, name='retrieve_particular_feedback'),
    path('<uuid:feedback_id>/delete/', views.delete_feedback_view, name='delete_feedback'),
    path('book/<uuid:book_isbn>/', views.get_all_feedbacks_on_a_book_view, name='retrieve_all_feedbacks_on_a_book')
]