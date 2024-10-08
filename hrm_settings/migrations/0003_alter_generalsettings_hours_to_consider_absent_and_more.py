# Generated by Django 5.0 on 2024-09-05 10:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_settings', '0002_generalsettings_hours_to_consider_absent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalsettings',
            name='hours_to_consider_absent',
            field=models.FloatField(default=2, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='hours_to_consider_half_Day',
            field=models.FloatField(default=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='shift_exceeded_time_to_considered_overtime',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
