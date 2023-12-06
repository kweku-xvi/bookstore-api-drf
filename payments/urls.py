from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:order_id>', views.checkout, name='initialize_payments'),
    path('webhook', views.payment_webhook, name='payment_webhook')
]