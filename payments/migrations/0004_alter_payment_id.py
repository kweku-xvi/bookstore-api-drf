# Generated by Django 5.0 on 2023-12-07 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_payment_options_payment_paid_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
