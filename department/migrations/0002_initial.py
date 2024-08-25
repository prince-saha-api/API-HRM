# Generated by Django 5.0 on 2024-08-25 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.ManyToManyField(blank=True, related_name='departmentone', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='departmenttwo', to=settings.AUTH_USER_MODEL),
        ),
    ]
