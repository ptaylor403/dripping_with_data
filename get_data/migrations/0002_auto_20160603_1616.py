# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawclockdata',
            name='PNCHEVNT_IN',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rawclockdata',
            name='PNCHEVNT_OUT',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
