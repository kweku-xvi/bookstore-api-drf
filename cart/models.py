import uuid
from django.db import models
from accounts.models import User
from books.models import Book


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.book.name} - Quantity {self.quantity}"

