# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-05 05:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
        ('payment_request_form', '0002_auto_20180605_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmaster',
            name='branch_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userapp.BranchMaster'),
        ),
    ]
