import random, string
from .models import Order
from cart.models import Cart, CartItem
from accounts.models import User
from accounts.permissions import IsVerified
from django.shortcuts import render, get_object_or_404
from payments.utils import initialize_transactions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsVerified])
def ordering_a_particular_book(request, item_id):
    if request.method == 'POST':
        try:
            user = request.user
            cart = get_object_or_404(Cart, user=user)
            cart_item = cart.items.get(id=item_id)

            amount = cart_item.quantity * cart_item.book.price

            order = Order.objects.create(
                user=request.user,
                total_amount=amount,
            )

            item = cart_item
            order.items.add(item)

            return Response(
                {
                    'success':True,
                    'message':'Order successfully placed',
                    'order_id':order.order_id
                }, status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response(
                {
                    'success':False,
                    'message':"Couldn't retrieve item. Provide a valid item ID"
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes([IsVerified])
def ordering_all_books_in_a_cart(request):
    if request.method == 'POST':
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        total_amount = 0

        if not cart:
            return Response(
                {
                    'success':False,
                    'message':'You have no books in your cart'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.all()

        for book in cart_items:
            total_amount += book.quantity * book.book.price

        order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
            )

        order.items.add(*cart_items)

        return Response(
                {
                    'success':True,
                    'message':'Order successfully placed',
                    'order_id':order.order_id
                }, status=status.HTTP_200_OK
            )