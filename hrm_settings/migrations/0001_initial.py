# Generated by Django 5.0 on 2024-08-25 08:20

import django.core.validators
import django.db.models.deletion
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
                ('from_month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20)),
                ('from_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('to_month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20)),
                ('to_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Generalsettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('fiscalyear_month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20)),
                ('workingday_starts_at', models.TimeField()),
                ('holiday_as_workingday', models.BooleanField(default=False)),
                ('consecutive_days_late_attendance_to_fine', models.IntegerField(default=3)),
                ('consecutive_late_attendance_to_fine', models.FloatField(default=100, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('fraction_of_daily_salary_for_halfday', models.FloatField(default=50, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('max_working_hours_against_timesheet', models.FloatField(default=8, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)])),
                ('basic_salary_percentage', models.FloatField(default=60, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('consider_attendance_on_holidays', models.CharField(choices=[('Disabled', 'Disabled'), ('Overtime', 'Overtime')], max_length=15)),
                ('allow_overtime', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Weekdays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('day', models.CharField(choices=[('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Weeklyholiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='fiscalyear',
            constraint=models.UniqueConstraint(fields=('from_month', 'to_month'), name='Fiscalyear_from_month_to_month'),
        ),
        migrations.AddField(
            model_name='generalsettings',
            name='fiscalyear',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm_settings.fiscalyear'),
        ),
        migrations.AddField(
            model_name='weeklyholiday',
            name='day',
            field=models.ManyToManyField(blank=True, to='hrm_settings.weekdays'),
        ),
        migrations.AddField(
            model_name='generalsettings',
            name='weekly_holiday',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm_settings.weeklyholiday'),
        ),
    ]
