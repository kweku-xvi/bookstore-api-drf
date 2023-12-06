import random, string
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from accounts.permissions import IsVerified
from books.models import Book
from django.shortcuts import render, get_object_or_404
from payments.utils import initialize_transactions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def generate_order_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


def get_book(book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)
        return book
    except Book.DoesNotExist:
        return Response(
            {
                'success':False,
                'error':'Book does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsVerified])
def add_book_to_cart(request, book_isbn):
    if request.method == 'POST':
        book = get_book(book_isbn=book_isbn)
        user = request.user

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_all_books_in_the_cart(request):
    if request.method == 'GET':
        user = request.user
        cart = user.cart.items

        serializer = CartItemSerializer(cart, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_cart_item(request, cart_id):
    if request.method == 'GET':
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_item = cart.items.get(id=cart_id)

        serializer = CartItemSerializer(cart_item)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def remove_cart_item(request, cart_id):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_item = cart.items.get(id=cart_id)

    if request.method == 'DELETE':
        cart_item.delete()

        return Response(
            {
                'success':True,
                'message':'Item has been successfully deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )


# @api_view(['POST'])
# @permission_classes([IsVerified])
# def order_particular_cart_item(request, cart_id):
#     if request.method == 'POST':
#         user = request.user
#         cart = get_object_or_404(Cart, user=user)
#         cart_item = cart.items.get(id=cart_id)

#         price = cart_item.quantity * cart_item.book.price

#         transaction = initialize_transactions(email=user.email, amount=str(price * 100), order_id=generate_order_id())

#         return Response (
#             {
#                 'success':True,
#                 'transaction_url':transaction,
#             }
#         )

# @api_view(['POST'])
# @permission_classes([IsVerified])
# def order_all_items_in_cart(request):
#     if request.method == 'POST':
#         price = 0

#         user = request.user
#         cart = get_object_or_404(Cart, user=user)
#         cart_items = cart.items.all()

        
#         for book in cart_items:
#             price += book.quantity * book.book.price


#         transaction = initialize_transactions(email=user.email, amount=str(price * 100), order_id=generate_order_id())

#         return Response (
#             {
#                 'success':True,
#                 'transaction_url':transaction,
#             }
#         )