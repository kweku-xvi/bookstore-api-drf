from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name', 'biography', 'image', 'birth_date', 'death_date', 'email', 'genre']
