# Generated by Django 5.0 on 2024-07-02 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiscalyear',
            name='from_month',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='fiscalyear',
            name='to_month',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
