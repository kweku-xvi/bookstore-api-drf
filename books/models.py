import uuid
from authors.models import Author
from django.core.validators import MinValueValidator
from django.db import models
from authors.models import Author


class Book(models.Model):
    BOOK_FORMAT = [
        ('Hardcover', 'Hardcover'),
        ('Paperback', 'Paperback'),
        ('Ebook', 'Ebook'),
        ('Other', 'Other')
    ]
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    isbn = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    format = models.CharField(max_length=255, choices=BOOK_FORMAT, default='Other')
    edition = models.CharField(max_length=255)
    date_published = models.DateField()
    cover_image = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=5.00, validators=[MinValueValidator(limit_value=0)])
    language = models.CharField(max_length=255, default='English')
    remaining_books = models.PositiveIntegerField(default=0, validators=[MinValueValidator(limit_value=0)])
    genre = models.CharField(max_length=255, blank=True, null=True, default='Other')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

