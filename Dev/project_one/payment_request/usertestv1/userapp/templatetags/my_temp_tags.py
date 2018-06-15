from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
	''' to check user group in template 
	'''
	group = Group.objects.get(name=group_name) 
	return group in user.groups.all()  