# Generated by Django 5.0 on 2024-07-18 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobrecord', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeejobhistory',
            old_name='prev_employee_typr',
            new_name='prev_employee_type',
        ),
    ]
