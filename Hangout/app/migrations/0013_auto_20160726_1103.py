# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20160724_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='state',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
