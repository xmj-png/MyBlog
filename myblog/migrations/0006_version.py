# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-08-09 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_counts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_nums', models.CharField(max_length=100, verbose_name='博客统计')),
            ],
            options={
                'verbose_name': '版本迭代',
                'verbose_name_plural': '版本迭代',
            },
        ),
    ]
