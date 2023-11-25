from django.db import models
import uuid
from accounts.models import User


class Payments(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.UUIDField(unique=True, default=uuid.uuid4)


    def __str__(self):
        return self.id
