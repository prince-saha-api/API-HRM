# Generated by Django 5.0 on 2024-08-13 07:20

import django.db.models.deletion
import helps.abstract.abstractclass
import notice.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch', '0005_remove_branch_user'),
        ('company', '0011_basicinformation_industry_type'),
        ('department', '0005_alter_department_branch'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticeboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to=notice.models.uploaddocs)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Noticeboardone', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Noticeboardtwo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Noticeboardbranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='branch.branch')),
                ('noticeboard', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='notice.noticeboard')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Noticeboardcompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('noticeboard', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='notice.noticeboard')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Noticeboarddepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('department', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='department.department')),
                ('noticeboard', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='notice.noticeboard')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Noticeboardemployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('noticeboard', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='notice.noticeboard')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
