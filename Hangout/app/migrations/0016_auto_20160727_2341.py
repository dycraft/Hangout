# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_activity_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='portrait',
            field=models.ImageField(upload_to='portrait'),
        ),
    ]