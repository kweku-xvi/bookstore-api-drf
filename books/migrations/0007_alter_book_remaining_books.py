# Generated by Django 4.2.1 on 2023-11-26 16:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_remove_book_quantity_book_remaining_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='remaining_books',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=0)]),
        ),
    ]