from rest_framework import serializers
from .models import User


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



class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ['id' ,'first_name', 'last_name', 'username', 'email', 'date_of_birth', 'created_at','password', 'token']

        read_only_fields = ['token']


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' ,'first_name', 'last_name', 'username', 'email', 'date_of_birth', 'created_at']


