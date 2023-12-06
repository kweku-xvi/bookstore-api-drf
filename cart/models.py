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
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.book.name} - Quantity {self.quantity}"


class OrderDetails(models.Model):
    order_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='cart_items')
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.order_id} - {self.user.username} - Total: {self.total_amount}"