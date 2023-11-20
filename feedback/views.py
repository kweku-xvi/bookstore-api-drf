from .models import Feedback
from .serializers import FeedbackSerializer
from books.models import Book
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


def get_book(request, book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)
    except Book.DoesNotExist:
        return Response(
            {
                'error':'This book does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )
    return book


def get_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
    except Feedback.DoesNotExist:
        return Response(
            {
                'error':'This feedback does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )
    return feedback
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_feedback_view(request, book_isbn): 
    if request.method == 'POST':
        book = get_book(book_isbn)

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
    if request.method == 'GET':
        feedback = get_feedback(feedback_id)

        serializer = FeedbackSerializer(feedback)

        return Response(
            {
                'success':True,
                'data':serializer.data,
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
def get_all_feedbacks_on_a_book_view(request, book_isbn):
    if request.method == 'GET':
        book = get_book(book_isbn)

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
    feedback = get_feedback(feedback_id)

    if request.method == 'DELETE':
        feedback.delete()

        return Response(
            {
                'success':True,
                'message':'The feedback has been deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@authentication_classes([])
def feedback_within_last_30_days(request, book_isbn):
    time_frame = timezone.now() - timedelta(days=30)

    if request.method == 'GET':
        book = get_book(book_isbn)

        feedbacks = Feedback.objects.filter(book=book, created_at__gte=time_frame)

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@authentication_classes([])
def feedback_within_last_3_months(request, book_isbn):
    time_frame = timezone.now() - timedelta(days=90)

    if request.method == 'GET':
        book = get_book(book_isbn)

        feedbacks = Feedback.objects.filter(book=book, created_at__gte=time_frame)

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


        
@api_view(['GET'])
@authentication_classes([])
def feedback_within_last_6_months(request, book_isbn):
    time_frame = timezone.now() - timedelta(days=180)

    if request.method == 'GET':
        book = get_book(book_isbn)

        feedbacks = Feedback.objects.filter(book=book, created_at__gte=time_frame)

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@authentication_classes([])
def feedback_within_last_year(request, book_isbn):
    time_frame = timezone.now() - timedelta(days=365)

    if request.method == 'GET':
        book = get_book(book_isbn)

        feedbacks = Feedback.objects.filter(book=book, created_at__gte=time_frame)

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )
