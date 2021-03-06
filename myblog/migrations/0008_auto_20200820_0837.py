# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-08-20 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0007_auto_20200809_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='PicTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='myblog/', verbose_name='图片名称')),
                ('pic_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='上传时间')),
            ],
            options={
                'verbose_name': '图片上传',
                'verbose_name_plural': '图片上传',
            },
        ),
        migrations.DeleteModel(
            name='Version',
        ),
    ]
