# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(verbose_name='created')),
                ('value_type', models.CharField(max_length=30)),
                ('time_type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30)),
                ('time', models.DateTimeField(verbose_name='time')),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Serie')),
            ],
        ),
    ]