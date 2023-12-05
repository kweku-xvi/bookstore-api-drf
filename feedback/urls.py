from django.urls import path
from . import views

urlpatterns = [
    path('<str:book_isbn>/add', views.add_feedback_view, name='add_feedback'),
    path('<uuid:feedback_id>', views.get_feedback_view, name='retrieve_particular_feedback'),
    path('<str:book_isbn>', views.get_all_feedbacks_on_a_book_view, name='retrieve_all_feedbacks_on_a_book'),
    path('<uuid:feedback_id>/delete', views.delete_feedback_view, name='delete_feedback'),
    
    path('book/<str:book_isbn>/last-30-days', views.feedback_within_last_30_days, name='feedback_within_last_30_days'),
    path('book/<str:book_isbn>/last-3-months', views.feedback_within_last_3_months, name='feedback_within_last_3_months'),
    path('book/<str:book_isbn>/last-6-months', views.feedback_within_last_6_months, name='feedback_within_last_6_months'),
    path('book/<str:book_isbn>/last-year', views.feedback_within_last_year, name='feedback_within_last_year'),
]