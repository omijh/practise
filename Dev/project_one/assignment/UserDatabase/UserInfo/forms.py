from django import forms
from .models import user_info

class UserForm(forms.ModelForm):
	class Meta:
		model = user_info
		fields = [
			"first_name",
			"last_name",
			"email",
			"mobile",
			"dob",
			"location"
		]