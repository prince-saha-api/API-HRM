# Generated by Django 5.0 on 2024-06-03 04:09

import helps.abstract.abstractclass
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(blank=True, default='admin', max_length=50, null=True)),
                ('password', models.CharField(blank=True, default='admin1234', max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('macaddress', models.CharField(blank=True, max_length=50, null=True)),
                ('deviceip', models.GenericIPAddressField(unpack_ipv4=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Devicegroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('device', models.ManyToManyField(blank=True, to='device.device')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
