# Generated by Django 5.0 on 2024-08-14 12:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_remove_user_basic_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='basic_salary',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
