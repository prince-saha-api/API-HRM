# Generated by Django 5.0 on 2024-07-02 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_settings', '0026_rename_days_weeklyholiday_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsettings',
            name='weekly_holiday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hrm_settings.weeklyholiday'),
        ),
    ]
