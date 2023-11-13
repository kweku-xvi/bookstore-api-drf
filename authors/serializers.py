from rest_framework import serializers
from .models import Author


class CreateAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'biography', 'image', 'birth_date', 'death_date', 'email', 'genre']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name', 'biography', 'image', 'birth_date', 'death_date', 'email', 'genre']
