# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlantSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('plant_code', models.CharField(max_length=3)),
                ('plant_target', models.IntegerField()),
                ('num_of_shifts', models.IntegerField()),
                ('first_shift', models.TimeField(blank=True, null=True)),
                ('second_shift', models.TimeField(blank=True, null=True)),
                ('third_shift', models.TimeField(blank=True, null=True)),
            ],
        ),
    ]
