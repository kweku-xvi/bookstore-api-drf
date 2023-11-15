import uuid
from books.models import Book
from django.db import models


class Feedback(models.Model):
    FEEDBACK_CATEGORIES = [
        ("Suggestion","Suggestion"),
        ("Complaint","Complaint"),
        ("Enquiry","Enquiry"),
        ("Other","Other"),
    ]

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    category = models.CharField(max_length=100, choices=FEEDBACK_CATEGORIES, default='Other')
    title = models.CharField(max_length=1255, blank=False, null=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

