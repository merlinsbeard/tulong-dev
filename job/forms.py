from django import forms
from django.forms import ModelForm
from job.models import Job, JobType
from ckeditor.widgets import CKEditorWidget
from comment.models import Comment
from person.models import Person, PersonClassification
import datetime
from django.forms.widgets import RadioSelect
from payment.models import PaymentType
from easy_maps.widgets import AddressWithMapWidget
from job.widgets import *
from message.models import Message

#from django_markdown.widgets import MarkdownWidget

CHOICES = (
	("Marikina City","Marikina City"),
	("Antipolo City","Antipolo City"),
	("Cainta","Cainta"),
	("Pasig City","Pasig City"),
	("Quezon City","Quezon City"),
	)

NUM_CHOICE = [(1,1),(2,2),(3,3),(4,4),(5,5)]

class JobPostForm(ModelForm):
	date_need = forms.DateField(label=(u'Date Need'),widget=forms.TextInput(attrs={"placeholder":"Date Need", "class": "datepicker",}))
	payment_type = forms.ModelChoiceField(queryset=PaymentType.objects.all(), empty_label="(Choose Payment Type)")
	job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), empty_label="(Choose Task Type)")
	#content = forms.CharField( widget=MarkdownWidget() )
	class Meta:
		model = Job
		fields = (
			'title',
			'content',
			'city',
			'address',
			'gmap',
			'job_type',
			'date_need',
			'number_employee',
			'payment_type',
			'duration',
			#'secret_detail',
			'amount',)
		
		widgets = {
			'gmap': LocationWidget()
		}
		

	def __init__(self, *args, **kwargs):
		super(JobPostForm, self).__init__(*args,**kwargs)
		self.fields['title'].widget = forms.TextInput(attrs={"placeholder":"Tutoring for 11 year old", })
		#self.fields['content'].widget = CKEditorWidget(config_name='awesome_ckeditor')
		self.fields['city'].widget = forms.RadioSelect(choices=CHOICES)
		self.fields['address'].widget = forms.Textarea(attrs={'rows':3, 'cols':15})
		#self.fields['secret_detail'].widget = forms.Textarea(attrs={'rows':5, 'cols':15, 'placeholder':'Secret Details Can only be seen by your chosen Kaakay. Post here important details that you do not want the public to see.'})
		self.fields['number_employee'] = forms.ChoiceField(widget=forms.Select(attrs={"class":"input-mini"}),choices=NUM_CHOICE, )
		self.fields['amount'].widget = forms.TextInput(attrs={"class":"input-small"})

		self.fields['title'].widget.attrs['class'] = 'form-control input-large'
		self.fields['content'].widget.attrs['class'] = 'form-control input-large'
		self.fields['address'].widget.attrs['class'] = 'form-control input-large'
		self.fields['job_type'].widget.attrs['class'] = 'form-control input-large'
		self.fields['date_need'].widget.attrs['class'] = 'form-control input-large'
		self.fields['number_employee'].widget.attrs['class'] = 'form-control input-large'
		self.fields['payment_type'].widget.attrs['class'] = 'form-control input-large'
		self.fields['duration'].widget.attrs['class'] = 'form-control input-large'
		self.fields['amount'].widget.attrs['class'] = 'form-control input-large'


	def clean_date_need(self):
		date_need = self.cleaned_data['date_need']
		if date_need < datetime.date.today():
			raise forms.ValidationError("The date cannot be in the past!")
		return date_need



class JobComment(ModelForm):

	class Meta:
		model = Comment
		exclude = ('commentor','job')

	def __init__( self, user, *args, **kwargs):
		self.job_slug = kwargs.pop('job_slug')
		super(JobComment, self).__init__( *args, **kwargs )
		self.user = user
		job = Job.objects.get(slug=self.job_slug)
		bidders = []
		doer = PersonClassification.objects.get(slug='doer')
		poster = PersonClassification.objects.get(slug='poster')
		fuck = [j for j in job.jobworker_set.all()]

		self.fields["receiver"].queryset = fuck
		