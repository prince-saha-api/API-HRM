# Generated by Django 5.0 on 2024-08-28 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userdevicegroup_userdevicegroup_user_devicegroup'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userdevicegroup',
            name='user_devicegroup',
        ),
    ]
