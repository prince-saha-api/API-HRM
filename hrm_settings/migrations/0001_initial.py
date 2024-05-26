# Generated by Django 5.0 on 2024-05-26 03:12

import django.core.validators
import helps.abstract.abstractclass
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fiscalyear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FixedWorkingdaysinamonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('days', models.IntegerField(default=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Latefineforfewdays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cost_in_days', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('consecutive', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workingminutesperday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('working_minutes_per_day', models.FloatField(default=540, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
