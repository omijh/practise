# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-06 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_request_form', '0010_auto_20180606_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmaster',
            name='gl_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentmaster',
            name='gl_desc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paymentmaster',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('APR', 'Approve'), ('DEC', 'Decline')], default='NEW', max_length=3),
        ),
    ]