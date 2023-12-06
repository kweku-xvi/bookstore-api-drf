import uuid
from accounts.models import User
from cart.models import Cart, CartItem
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_amount = models.DecimalField(max_digits=14, decimal_places=4, default=0.00, validators=[MinValueValidator(limit_value=0)])
    date_ordered = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id} - By {self.user.username} - Total: {self.total_amount}"

    class Meta:
        ordering = ('-created_at',)