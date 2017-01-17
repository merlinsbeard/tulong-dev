from django import forms
from django.forms import ModelForm
from discussion.models import Discussion

class DiscussionForm(ModelForm):
	class Meta:
		model = Discussion
		fields = ( 'message',)