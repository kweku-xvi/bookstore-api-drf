import os, jwt
from .models import User
from .serializers import RegisterUserSerializer, LoginSerializer, UsersSerializer
from .utils import send_password_reset_email, send_verification_email
from dotenv import load_dotenv
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

load_dotenv()


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

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_user')
            absolute_url = f'http://{current_site}{relative_link}?token={token}'
            link = str(absolute_url)
            send_verification_email(email=user.email, username=user.username, link=link)

            return Response(
                {
                    'success':True,
                    'message':'Account created successfully',
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'error':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def verify_user_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')   

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_verified:
                user.is_verified = True
                user.save()
            
            return Response(
                {
                    'success':True,
                    'message':'Email has been successfully verified'
                }, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as e:
            return Response(
                {
                    'success':False,
                    'message':'Activation link expired'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.InvalidTokenError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist as e:
            return Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@authentication_classes([])
def login_user_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tokens = serializer.generate_jwt_tokens(serializer.validated_data)

            return Response(
                {
                    'success':True,
                    'message':'Login successful!',
                    'tokens':tokens
                }, status=status.HTTP_200_OK
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
        
# @api_view(['POST'])
# def password_reset_view(request):
#     if request.method == "POST":
#         email = request.data.get('email')
#         if not email:
#             return Response(
#                 {
#                     "success":False,
#                     "message":"Email is required",
#                 },status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             user = User.objects.get(email=email)
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             current_site = get_current_site(request).domain
#             relative_link = reverse('password_reset_confirm_view')
#             absolute_url = f'http://{current_site}{relative_link}?uid={uid}&token={token}'
#             link = str(absolute_url)
#             send_password_reset_email(link=link,email=email, username=user.username)
#             return Response(
#                 {
#                     "success":True,
#                     "message":"Password Reset Email Sent",
#                 },status=status.HTTP_200_OK
#             )
#         except User.DoesNotExist as e:
#             return Response(
#                 {
#                     "success":False,
#                     "message":"User Does Not Exist",
#                 },status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "success":False,
#                     "message":str(e),
#                 },status=status.HTTP_400_BAD_REQUEST
#             )


# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def reset_password_confirm_view(request):
#     if request.method == "PATCH":
#         uid = request.data.get("uid")
#         token = request.data.get("token")
#         password = request.data.get("password")
#         if not uid or not token or not password:
#             return Response(
#                 {
#                     "success":False,
#                     "message":"All Fields Are Required",
#                 },status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             user_id = urlsafe_base64_decode(uid)
#             user = User.objects.get(id=user_id)
#             if not default_token_generator.check_token(user,token):
#                 return Response(
#                     {
#                         "success":False,
#                         "message":"Invalid Token",
#                     },status=status.HTTP_400_BAD_REQUEST
#                 )
#             user.set_password(password)
#             user.save()
#             return Response(
#                 {
#                     "success":True,
#                     "message":"Password Reset Successful",
#                 },status=status.HTTP_200_OK
#             )
#         except User.DoesNotExist as e:
#             return Response(
#                 {
#                     "success":False,
#                     "message":"User Does Not Exist",
#                 },status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "success":False,
#                     "message":str(e),
#                 },status=status.HTTP_400_BAD_REQUEST
#             )


@api_view(['POST'])
def password_reset_view(request):
    if request.method == 'POST':
        email = request.data.get('email')

        if not email:
            return Response(
                {
                    'success':False,
                    'message':'Email is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request).domain
            relative_link = reverse('password_reset_confirm')
            absolute_url = f'http://{current_site}{relative_link}?uid={uid}&token={token}'
            link = str(absolute_url)
            send_password_reset_email(email=user.email, username=user.username, link=link)

            return Response(
                {
                    'success':True,
                    'message':'Password reset email successfully sent!'
                }, status=status.HTTP_200_OK
            )
        except User.DoesNotExist as e:
            return Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['PATCH'])
def password_reset_confirm_view(request):
    if request.method == 'PATCH':
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uid or not token or not password:
            return Response(
                {
                    'success':False,
                    'message':'All the fields are required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(id=user_id)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {
                        'success':False,
                        'message':'Invalid token'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.save()

            return Response(
                {
                    'success':True,
                    'message':'Password has been reset'
                }, status=status.HTTP_200_OK
            )

        except User.DoesNotExist as e:
            return Response(
                    {
                        'success':False,
                        'message':'User does not exist'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                    {
                        'success':False,
                        'message':str(e)
                    }, status=status.HTTP_400_BAD_REQUEST
                )