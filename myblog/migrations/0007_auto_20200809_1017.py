# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-08-09 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0006_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='blog_nums',
            field=models.CharField(max_length=100, verbose_name='博客版本'),
        ),
    ]
