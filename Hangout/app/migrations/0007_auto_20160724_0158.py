# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 01:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_activity_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 24, 1, 58, 2, 504339, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 7, 24, 1, 58, 17, 9744, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 24, 1, 58, 18, 985490, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='intro',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(default='', max_length=50),
        ),
    ]
