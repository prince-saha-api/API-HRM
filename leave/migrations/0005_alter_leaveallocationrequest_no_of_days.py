# Generated by Django 5.0 on 2024-07-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_alter_leavesummary_fiscal_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveallocationrequest',
            name='no_of_days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
