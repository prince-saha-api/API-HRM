# Generated by Django 5.0 on 2024-05-30 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
