# Generated by Django 4.2.1 on 2023-12-06 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 6, 14, 22, 8, 281571, tzinfo=datetime.timezone.utc)),
        ),
    ]