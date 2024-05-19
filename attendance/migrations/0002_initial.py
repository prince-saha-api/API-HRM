# Generated by Django 5.0 on 2024-05-19 05:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        ('officialoffday', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='office_off_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='officialoffday.offday'),
        ),
        migrations.AddField(
            model_name='devicelogs',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='remotelogs',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestmanualattendance',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requestmanualattendancetwo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestmanualattendance',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requestmanualattendanceone', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestremoteattendance',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requestremoteattendancetwo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestremoteattendance',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requestremoteattendanceone', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(fields=('date', 'employee'), name='Attendance_date_employee'),
        ),
        migrations.AddConstraint(
            model_name='devicelogs',
            constraint=models.UniqueConstraint(fields=('employee', 'date', 'in_time'), name='Devicelogs_employee_date_in_time'),
        ),
        migrations.AddConstraint(
            model_name='remotelogs',
            constraint=models.UniqueConstraint(fields=('employee', 'date', 'time'), name='Remotelogs_employee_date_time'),
        ),
        migrations.AddConstraint(
            model_name='requestmanualattendance',
            constraint=models.UniqueConstraint(fields=('requested_by', 'date'), name='Requestmanualattendance_requested_by_date'),
        ),
        migrations.AddConstraint(
            model_name='requestremoteattendance',
            constraint=models.UniqueConstraint(fields=('requested_by', 'date'), name='Requestremoteattendance_requested_by_date'),
        ),
    ]
