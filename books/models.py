import uuid
from authors.models import Author
from django.db import models
from djmoney.models.fields import MoneyField
from authors.models import Author


class Book(models.Model):
    BOOK_FORMAT = [
        ('Hardcover', 'Hardcover'),
        ('Paperback', 'Paperback'),
        ('Ebook', 'Ebook'),
        ('Other', 'Other')
    ]

    isbn = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.IntegerField(default=0)
    format = models.CharField(max_length=255, choices=BOOK_FORMAT, default='Other')
    edition = models.CharField(max_length=255)
    date_published = models.DateField()
    cover_image = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=5.00)
    language = models.CharField(max_length=255, default='English')
    quantity = models.IntegerField(default=0)
    genre = models.CharField(max_length=255, blank=True, null=True, default='Other')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

