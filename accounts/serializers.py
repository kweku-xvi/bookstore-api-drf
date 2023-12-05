from .models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'created_at','password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already in use')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already in use')

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            date_of_birth=validated_data['date_of_birth']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, min_length=8)


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials', code='authentication')

        attrs['user'] = user
        return attrs

    
    def generate_jwt_tokens(self, attrs):
        user = attrs.get('user')

        refresh_token = RefreshToken.for_user(user)

        tokens = {
            'refresh':str(refresh_token),
            'access':str(refresh_token.access_token)
        }

        return tokens


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' ,'first_name', 'last_name', 'username', 'email', 'date_of_birth', 'created_at']


