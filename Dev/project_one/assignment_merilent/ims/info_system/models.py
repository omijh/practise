# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

vendors = (
	('IBM', 'IBM Computers'),
	('MST','Microsoft'),
	('APL','Apple'),
	('ADB','Adobe'),
	('AMZ','Amazon'),
	('TAT','Tata')
	)

class info_sys(models.Model):

	item_name = models.CharField(max_length=200)
	description = models.TextField()
	cost = models.FloatField()
	vendor = models.CharField(max_length=3, choices=vendors)
	isActive = models.BooleanField(default=True)

	def __str__(self):
		return self.item_name
