# Generated by Django 5.0 on 2024-05-28 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestmanualattendance',
            old_name='approved_by',
            new_name='decisioned_by',
        ),
    ]
