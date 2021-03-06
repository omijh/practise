# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-05 03:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_request_form', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmaster',
            name='bank_account_no',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='date',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='ifsc_code',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='invoice_number',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='name_of_bank',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='name_of_party',
        ),
        migrations.RemoveField(
            model_name='paymentmaster',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='paymentmaster',
            name='nature_of_expenses',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
