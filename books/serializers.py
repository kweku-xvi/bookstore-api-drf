from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'name', 'description', 'rating', 'format', 'edition', 'date_published', 'cover_image']

class UpdateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'name', 'description', 'rating', 'format', 'edition', 'date_published', 'cover_image', 'author']