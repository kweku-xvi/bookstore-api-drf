from .models import CartItem
from books.serializers import BookSerializer
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = CartItem
        fields = ['id','book', 'quantity']