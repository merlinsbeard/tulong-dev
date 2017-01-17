from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from person.models import Person

class LoginForm(forms.Form):
	username        = forms.CharField(label=(u'Email'), widget=forms.TextInput(attrs={"placeholder":"Email", }))
	password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False, attrs={"placeholder":"Password",}))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.get(username=username)
			person = Person.objects.get(person=user)
			return username
		except User.DoesNotExist:
			raise forms.ValidationError("Email not existing")

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control input-large'
		self.fields['password'].widget.attrs['class'] = 'form-control input-large'
            
			
