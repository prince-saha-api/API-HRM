# Generated by Django 5.0 on 2024-05-21 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_perdaysalary_calculation_based_on_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Salary',
        ),
    ]
