# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-06 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_request_form', '0013_auto_20180606_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmaster',
            name='updated_by',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
