# Generated by Django 5.0 on 2024-06-04 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavepolicy',
            name='applicable_for',
        ),
    ]
