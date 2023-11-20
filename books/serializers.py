from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['isbn', 'name', 'description', 'rating', 'format', 'edition', 'date_published', 'cover_image', 'author']
    
    def get_author(self, obj):
        return obj.author.name if obj.author else None