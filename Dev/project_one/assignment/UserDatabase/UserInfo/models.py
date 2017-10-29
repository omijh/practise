# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import pre_save
from django.db import models
from django.utils.text import slugify
# Create your models here.
class user_info(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	mobile = models.IntegerField()
	dob = models.DateTimeField()
	location = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.first_name

def pre_save_receiver(sender,instance,*args,**kwargs):
	slug = slugify(str(instance.first_name)+str(instance.last_name))
	exists = user_info.objects.filter(slug=slug).exists()
	if exists:
		slug = "%s-%s"%(slug, instance.id)
	instance.slug = slug
pre_save.connect(pre_save_receiver,sender=user_info)

