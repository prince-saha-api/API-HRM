# Generated by Django 5.0 on 2024-07-02 09:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_settings', '0018_rename_consecutivelateattendancetofine_consecutivelateattendance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consecutivelateattendance',
            old_name='count',
            new_name='days_to_fine',
        ),
        migrations.AddField(
            model_name='consecutivelateattendance',
            name='fine_amount_percentage',
            field=models.FloatField(default=100, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
