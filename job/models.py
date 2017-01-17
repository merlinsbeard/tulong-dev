from django.db import models
from payment.models import PaymentType
from person.models import Person
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from job.widgets import *

CHOICES = (
	("Marikina City","Marikina City"),
	("Antipolo City","Antipolo City"),
	("Cainta","Cainta"),
	("Pasig City","Pasig City"),
	("Quezon City","Quezon City"),
	)

class JobType(models.Model):
	job_type 	= models.CharField(max_length=200)
	description = models.TextField()
	slug 		= models.SlugField(unique=True, max_length=200)
	image 		= models.ImageField(upload_to="media/images/jobcat", blank=True, default='media/images/jobcat/default.jpg')
	def __unicode__(self):
		return self.job_type

	@models.permalink
	def get_absolute_url(self):
		return ('job:cat',(), {'slug':self.slug})

class JobDuration(models.Model):
	duration_type=models.CharField(max_length=100)
	description	 = models.TextField()
	slug 		 = models.SlugField(unique=True)

	def __unicode__(self):
		return self.duration_type

class Job(models.Model):
	title			= models.CharField(max_length=255)
	slug 			= models.SlugField(unique=True,max_length=255, blank=True, default='')
	content 		= models.TextField()
	number_employee = models.IntegerField(default=1)
	payment_type	= models.ForeignKey(PaymentType)
	duration 		= models.ForeignKey(JobDuration)
	job_type 		= models.ForeignKey(JobType)
	creator 		= models.ForeignKey(Person)
	amount			= models.DecimalField(max_digits=8, decimal_places=2)
	address 		= models.TextField()
	gmap 			= models.TextField()
	city 			= models.CharField(max_length=100,choices=CHOICES)
	secret_detail	= models.TextField(blank=True)
	is_published 	= models.BooleanField(default=True)
	has_winner 		= models.BooleanField(default=False)
	is_close		= models.BooleanField(default=False)
	is_sticky 		= models.BooleanField(default=False)
	is_payed 		= models.BooleanField(default=False)
	is_done 		= models.BooleanField(default=False)
	date_need 		= models.DateTimeField()
	created_at		= models.DateTimeField(auto_now_add=True, editable=False)
	updated_at 		= models.DateTimeField(auto_now=True, editable=False)


	class Meta:
		ordering=['is_done','-created_at', ]

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Job, self).save(*args, **kwargs)
		if not self.slug:
			words =str(self.creator.id)+" "+self.title+" "+str(self.id)
			self.slug = slugify(words)
			self.save()

	@models.permalink
	def get_absolute_url(self):
		return ('job:detail',(), {'slug':self.slug})

	

class JobWorker(models.Model):
	worker = models.ForeignKey(Person)
	job = models.ForeignKey(Job)
	date_hired = models.DateTimeField(auto_now_add=True, editable=False)

	def __unicode__(self):
		word = '%s %s' % (self.worker, self.job)
		return word
