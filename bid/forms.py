from django import forms
from django.forms import ModelForm
from bid.models import Bid
from job.models import Job
from person.models import Person



class BidForm(ModelForm):
	class Meta:
		model = Bid
		fields =('amount','message',)

	
	def __init__( self, user, *args, **kwargs):
		self.fuck = kwargs.pop('fuck')
		super(BidForm, self).__init__( *args, **kwargs )
		self.user = user
		self.fields['message'].widget = forms.Textarea(attrs={'rows':3, 'cols':15})
		
	def clean(self):
		job = self.fuck
		poster = Person.objects.get(person=self.user)
		checking = Bid.objects.filter(job=job, bidder=poster)
		if Bid.objects.filter(job=job, bidder=poster):
			raise forms.ValidationError("Already Bid!")
		else:
			return self.cleaned_data
			