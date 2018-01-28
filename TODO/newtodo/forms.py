from django import forms
from newtodo.models import Signup

class signupform(forms.ModelForm):
	name = forms.CharField()  # Field name made lowercase.
	email = forms.CharField()
	passwd = forms.CharField()
	class Meta:
		model=Signup
		fields='__all__'