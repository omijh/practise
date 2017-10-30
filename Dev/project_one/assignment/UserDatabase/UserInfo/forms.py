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

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
		})