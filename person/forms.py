from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from person.models import Person, PersonSkills
from datetime import datetime

class UpdateInform(ModelForm):
	skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
									queryset=PersonSkills.objects.all(), required=False)

	class Meta:
		model = Person
		fields = ('firstname','lastname',
			'address','image', 'info', 
			'skills', 'badge', 'is_verified',
			'is_active')

	def __init__(self, *args, **kwargs):
		super(UpdateInform, self).__init__(*args,**kwargs)
		self.fields['address'].widget = forms.Textarea(attrs={'rows':3,})
		self.fields['firstname'].widget.attrs['class'] = 'form-control input-large'
		self.fields['lastname'].widget.attrs['class'] = 'form-control input-large'
		self.fields['info'].widget.attrs['class'] = 'form-control input-large'
		self.fields['address'].widget.attrs['class'] = 'form-control input-large'




		

