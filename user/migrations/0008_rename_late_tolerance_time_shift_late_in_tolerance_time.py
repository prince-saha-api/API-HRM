# Generated by Django 5.0 on 2024-09-05 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_shift_early_leave_tolerance_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='late_tolerance_time',
            new_name='late_in_tolerance_time',
        ),
    ]
