# Generated by Django 5.0 on 2024-05-21 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_rename_role_rolepermission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role_permission',
            field=models.ManyToManyField(blank=True, to='user.rolepermission'),
        ),
    ]
