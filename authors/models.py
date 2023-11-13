import uuid
from django.db import models


class Author(models.Model):
    id =  models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    biography = models.TextField()
    image = models.ImageField(blank=True, null=True)
    birth_date = models.DateField(blank=False, null=False)
    death_date = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    genre = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']