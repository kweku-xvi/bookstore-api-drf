from django.urls import path
from . import views

urlpatterns = [
    path('', views.initialize_payments, name='initialize_payments'),
    path('webhook', views.payment_webhook, name='payment_webhook')
]