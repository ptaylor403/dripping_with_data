# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-12 22:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


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
                ('plant_code', models.CharField(default='017', max_length=3)),
                ('plant_target', models.IntegerField(default=55)),
                ('num_of_shifts', models.IntegerField(default=2)),
                ('first_shift', models.TimeField(blank=True, default=datetime.time(6, 30), null=True)),
                ('second_shift', models.TimeField(blank=True, default=datetime.time(14, 30), null=True)),
                ('third_shift', models.TimeField(blank=True, default=datetime.time(22, 30), null=True)),
                ('dripper_start', models.DateTimeField(default=datetime.datetime(2016, 4, 1, 4, 0, tzinfo=utc))),
            ],
        ),
    ]
