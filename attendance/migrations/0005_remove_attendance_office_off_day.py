# Generated by Django 5.0 on 2024-07-02 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_attendance_office_off_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='office_off_day',
        ),
    ]
