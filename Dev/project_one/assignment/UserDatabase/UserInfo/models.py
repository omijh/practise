# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator

class user_info(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.EmailField()
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	mobile = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list
	dob = models.DateField()
	location = models.CharField(max_length=200)

	def __str__(self):
		return self.first_name


