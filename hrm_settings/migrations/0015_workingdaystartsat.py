# Generated by Django 5.0 on 2024-07-02 08:43

import helps.abstract.abstractclass
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_settings', '0014_delete_fixedworkingdaysinamonth_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workingdaystartsat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.TimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
