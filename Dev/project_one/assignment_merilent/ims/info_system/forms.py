from django import forms
from .models import info_sys


class Info_sys(forms.ModelForm):
	class Meta:
		model = info_sys
		fields = [
			"id",
			"item_name",
			"description",
			"cost",
			"vendor",
		]

