# Generated by Django 5.0 on 2024-09-03 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='working_minutes',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
