# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 13:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_relationship_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 27, 13, 37, 0, 862472, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
