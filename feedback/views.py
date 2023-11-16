from .models import Feedback
from .serializers import FeedbackSerializer
from books.models import Book
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_feedback_view(request, book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)
    except Book.DoesNotExist:
        return Response (
            {
                'error':'This book does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(book=book, user=request.user)

            return Response (
                {
                    'success':True,
                    'data':serializer.data,
                }, status=status.HTTP_201_CREATED
            )
        return Response (
            {
                'success':False,
                'data':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@authentication_classes([])
def get_feedback_view(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
    except Feedback.DoesNotExist:
        return Response(
            {
                'error':'This feedback does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = FeedbackSerializer(feedback)

        return Response(
            {
                'success':True,
                'data':serializer.data,
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
def get_all_feedbacks_on_a_book_view(request, book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)
    except Book.DoesNotExist:
        return Response(
            {
                'error':'This book does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        feedbacks = Feedback.objects.filter(book=book)

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data,
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_feedback_view(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
    except Feedback.DoesNotExist:
        return Response(
            {
                'error':'This feedback does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'DELETE':
        feedback.delete()

        return Response(
            {
                'success':True,
                'message':'The feedback has been deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )