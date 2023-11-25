from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .utils import initialize_transactions
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initialize_payments(request):
    user = request.user
    email = user.email

    transaction = initialize_transactions(email=email, amount='100', order_id='kyyya74ajdo25if8ag')

    return Response (
        {
            'success':True,
            'transaction_url':transaction,
        }
    )


@api_view(['POST'])
@authentication_classes([])
def payment_webhook(request):
    payload = json.loads(request.body)

    event = payload['event']
    data = payload['data']

    if event == 'charge.success':
        reference = data['reference']

    return Response(
        {
            'success':True,
            'reference_id':reference,
        }, status=status.HTTP_200_OK
    )
