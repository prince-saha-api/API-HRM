# Generated by Django 5.0 on 2024-06-03 04:09

import django.db.models.deletion
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
        migrations.AddField(
            model_name='departmentemail',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
        migrations.AddField(
            model_name='departmentimage',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
        migrations.AddField(
            model_name='departmentmobilenumber',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
    ]
