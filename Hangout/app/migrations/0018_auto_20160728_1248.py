# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160728_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='feature',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='user',
            name='feature',
            field=models.CharField(default='', max_length=300),
        ),
    ]
