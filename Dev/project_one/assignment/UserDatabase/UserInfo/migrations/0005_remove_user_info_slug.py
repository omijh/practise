# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 03:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0004_auto_20171030_0348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_info',
            name='slug',
        ),
    ]
