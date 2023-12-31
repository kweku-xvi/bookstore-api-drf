from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'isbn', 'cover_image','description', 'edition', 'format', 'date_published', 'genre', 'rating', 'author','price', 'language', 'remaining_books']
    
    def get_author(self, obj):
        return obj.author.name if obj.author else None