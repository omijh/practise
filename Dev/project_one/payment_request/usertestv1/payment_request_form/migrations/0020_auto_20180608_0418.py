# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-08 04:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_request_form', '0019_auto_20180607_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmaster',
            name='approval_date_lvl1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paymentmaster',
            name='approval_date_lvl2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paymentmaster',
            name='approval_date_lvl3',
            field=models.DateField(blank=True, null=True),
        ),
    ]
