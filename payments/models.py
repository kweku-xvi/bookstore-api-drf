from django.db import models
from django.core.validators import MinValueValidator
import uuid
from accounts.models import User
from orders.models import Order
from django.utils import timezone

class Payment(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, validators=[MinValueValidator(limit_value=0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return F'Payment #{self.id} - {self.user.username} - Amount: {self.amount}'

    class Meta:
        ordering = ('-paid_at', )
