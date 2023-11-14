import uuid
from authors.models import Author
from django.db import models
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

