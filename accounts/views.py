from .models import User
from .serializers import RegisterUserSerializer, LoginUserSerializer, UsersSerializer
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auth_user_api_view(request):
    user = request.user
    serializer = RegisterUserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
def create_user_view(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)

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
                'error':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@authentication_classes([])
def login_user_view(request):
    if request.method == 'POST':
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = LoginUserSerializer(user)

            return Response(
                {
                    'success':True,
                    'data':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':False,
                'errors':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def retrieve_all_users_view(request):
    if request.method == 'GET':
        users = User.objects.all()

        serializer = UsersSerializer(users, many=True)

        return Response(
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )
        

# Todo : Email verification & Password Reset