# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='state',
            field=models.IntegerField(default=0),
        ),
    ]
