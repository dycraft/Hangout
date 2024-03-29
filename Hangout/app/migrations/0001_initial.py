# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('intro', models.CharField(max_length=1000)),
                ('cost', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Following'), (2, 'Blocked')])),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('cellphone', models.CharField(max_length=20)),
                ('score', models.FloatField(default=0.0)),
                ('portrait', models.ImageField(upload_to='')),
                ('email', models.URLField()),
                ('fix_times', models.IntegerField(default=0)),
                ('tmp_times', models.IntegerField(default=0)),
                ('admin_acts', models.ManyToManyField(related_name='admins', to='app.Activity')),
                ('apply_acts', models.ManyToManyField(related_name='applicants', to='app.Activity')),
                ('coll_acts', models.ManyToManyField(related_name='collected', to='app.Activity')),
                ('follow', models.ManyToManyField(related_name='followed', through='app.Relationship', to='app.User')),
                ('join_acts', models.ManyToManyField(related_name='members', to='app.Activity')),
                ('tags', models.ManyToManyField(related_name='users', to='app.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='relationship',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to='app.User'),
        ),
        migrations.AddField(
            model_name='relationship',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to='app.User'),
        ),
        migrations.AddField(
            model_name='notice',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_notice', to='app.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='app.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app.User'),
        ),
        migrations.AddField(
            model_name='activity',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_acts', to='app.User'),
        ),
        migrations.AddField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(related_name='acts', to='app.Tag'),
        ),
    ]
