from django.shortcuts import render
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .utils import initialize_transactions, verify_payment,  generate_payment_id
from .models import Payment
from accounts.models import User
import json, random, string
from orders.models import Order
from accounts.permissions import IsVerified

@api_view(['POST'])
@permission_classes([IsVerified])
def checkout(request, order_id):
    if request.method == 'POST':
        user = request.user 
        email = user.email 

        try:
            order = Order.objects.get(order_id=order_id)

            transaction = initialize_transactions(email=email, amount=str(100 * order.total_amount), payment_id=generate_payment_id())

            return Response(
                    {
                        'success':True,
                        'transaction_url':transaction
                    }, status=status.HTTP_200_OK
                )
        except Order.DoesNotExist:
            return Response(
                {
                    'success':False,
                    'message':'The order does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        

@api_view(['POST'])
@authentication_classes([])
def payment_webhook(request):
    payload = json.loads(request.body)

    event = payload['event']
    data = payload['data']

    if event == 'charge.success':
        reference = data['reference']

        payment = Payment.objects.create(
            amount=data['amount'] / 100,
            user=User.objects.get(email=data['customer']['email']),
            order=None,
            paid_at=data['paid_at']
        )

    return Response(
        {
            'success':True,
            'reference_id':reference,
        }, status=status.HTTP_200_OK
    )


