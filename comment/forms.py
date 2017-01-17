from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from comment.models import Comment
from person.models import Person
from bid.models import Bid
from job.models import Job

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = (
			'receiver',
			'rating',
			'comment',
			)

	def __init__( self, user, *args, **kwargs):
		self.job = kwargs.pop('fuck')
		super(CommentForm, self).__init__(*args,**kwargs)
		self.user = user
		bids = Bid.objects.filter(job=self.job,is_chosen=True)
		list_of_pk = []
		person = Person.objects.get(person=self.user)
		if person.person_class.slug=='doer':
			list_of_pk.append(self.job.creator.id)
		else:
			for bid in bids:
				list_of_pk.append(bid.bidder.id)
		receivers=Person.objects.filter(pk__in=list_of_pk)
		
		self.fields['receiver'].queryset=receivers

