# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-05 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_request_form', '0008_paymentmaster_head_of_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmaster',
            name='bank_acc_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
