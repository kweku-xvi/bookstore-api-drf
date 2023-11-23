from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['isbn', 'name', 'cover_image','description', 'edition', 'format', 'date_published', 'genre', 'rating', 'author','price', 'language', 'quantity']
    
    def get_author(self, obj):
        return obj.author.name if obj.author else None