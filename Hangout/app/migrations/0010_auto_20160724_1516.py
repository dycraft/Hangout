# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 07:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 24, 7, 16, 15, 597611, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='state',
            field=models.IntegerField(choices=[(0, 'open'), (1, 'started'), (2, 'ended')], default=0),
        ),
        migrations.AlterField(
            model_name='application',
            name='application_type',
            field=models.IntegerField(choices=[(1, 'member'), (2, 'admin')], default=1),
        ),
    ]