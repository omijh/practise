# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-07 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_request_form', '0016_paymentmaster_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmaster',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]