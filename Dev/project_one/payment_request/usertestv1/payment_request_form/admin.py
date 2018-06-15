# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import HeadOfAccounts,PaymentMaster

admin.site.register(HeadOfAccounts)
admin.site.register(PaymentMaster)

# Register your models here.
