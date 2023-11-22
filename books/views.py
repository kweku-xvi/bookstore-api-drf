from .models import Book
from .serializers import BookSerializer
from authors.models import Author
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


def get_book(book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)
        return book 
    except Book.DoesNotExist:
        return Response(
            {
                'message':'This book does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )


def get_author(author_id):
    try:
        author = Author.objects.get(id=author_id)
        return author
    except Author.DoesNotExist:
        return Response(
            {
                'message':'This author does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book_view(request, author_id):
    if request.method == 'POST':
        book_author = get_author(author_id)
        
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=book_author)

            return Response(
                {
                    'success':True,
                    'data':serializer.data,
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'data':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@authentication_classes([])
def retrieve_book_view(request, book_isbn):
    if request.method == 'GET':
        book = get_book(book_isbn)

        serializer = BookSerializer(book)

        return Response(
            {
                'success':True,
                'data':serializer.data,
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@authentication_classes([])
def retrieve_books_by_author(request, author_id):
    if request.method == 'GET':
        author = get_author(author_id)

        books = Book.objects.filter(author=author)

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_book_details_view(request, book_isbn):
    if request.method == 'PUT' or request.method == 'PATCH':
        book = get_book(book_isbn)

        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'data':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book_view(request, book_isbn):
    book = get_book(book_isbn)

    if request.method == 'DELETE':
        book.delete()

        return Response(
            {
                'success':True,
                'message':'The book has been deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@authentication_classes([])
def filter_books_by_genre_or_rating_view(request):
    if request.method == 'GET':
        books = Book.objects.all()
        genre = request.query_params.get('genre')
        rating = request.query_params.get('rating')

        if genre and not rating:
            books = books.filter(genre__iexact=genre)
        elif rating and not genre:
            books = books.filter(rating__iexact=rating)
        elif rating and genre:
            books = books.filter(genre__iexact=genre, rating__iexact=rating)
        else:
            return Response(
                {
                    'error':'Please provide filter query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@authentication_classes([])
def search_books_view(request):
    if request.method == 'GET':
        query = request.query_params.get('query')

        if not query:
            return Response(
                {
                    'error':'Please provide a search query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        books = Book.objects.filter(
            Q(name__icontains=query) |
            Q(author__name__icontains=query) |
            Q(genre__icontains=query)
        )

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'message':'Below are your search results',
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )