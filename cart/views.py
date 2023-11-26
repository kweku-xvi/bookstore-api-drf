from .models import Cart, CartItem
from .serializers import CartItemSerializer
from books.models import Book
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_book_from_cart(request, book_isbn):
    book = get_book(book_isbn=book_isbn)

    cart_item = CartItem.objects.get(book=book)

    if request.method == 'DELETE':
        cart_item.delete()

        return Response(
            {
                'success':True,
                'message':'Item has been successfully deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )