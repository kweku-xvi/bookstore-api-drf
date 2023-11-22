from .models import Author
from .serializers import CreateAuthorSerializer, AuthorSerializer
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_author_view(request):
    if request.method == 'POST':
        serializer = CreateAuthorSerializer(data=request.data)

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
                'errors':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@authentication_classes([])
def retrieve_author_view(request, author_id): # retrieves specific author
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({'error':'The author does not  exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AuthorSerializer(author)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )



@api_view(['GET'])
@permission_classes([IsAdminUser])
def retrieve_all_authors(request): # retrieves all authors 
    if request.method == 'GET':
        authors = Author.objects.all()

        serializer = AuthorSerializer(authors, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_author_view(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({'error':'The author does not  exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = AuthorSerializer(author, data=request.data, partial=True)

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
                'errors':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )
        

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_author_view(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({'error':'The author does not  exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method  == 'DELETE':
        author.delete()

        return Response(
            {
                'success':True,
                'message':'Author deleted!'
            }, status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@authentication_classes([])
def filter_authors_by_genre_view(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        genre = request.query_params.get('genre')

        if genre:
            authors = authors.filter(genre__iexact=genre)
        else:
            return Response(
                {
                    'error':'Please provide a filter query'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AuthorSerializer(authors, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@authentication_classes([])
def search_authors_by_name_or_genre_view(request):
    if request.method == 'GET':
        query = request.query_params.get('query')

        if not query:
            return Response (
                {
                    'error':'Please provide search query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        authors = Author.objects.filter(
            Q(name__icontains=query) |
            Q(genre__icontains=query)
        )

        serializer = AuthorSerializer(authors, many=True)

        return Response(
            {
                'success':True,
                'message':'Below are your search results',
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )