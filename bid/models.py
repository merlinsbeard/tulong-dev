from django.db import models
from job.models import Job 
from person.models import Person 

class Bid(models.Model):
	job = models.ForeignKey(Job)
	bidder = models.ForeignKey(Person)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	is_chosen = models.BooleanField(default=False)
	created_at	= models.DateTimeField(auto_now_add=True, editable=False)
	message = models.TextField()

	def __unicode__(self):
		word = str(self.job)+" "+str(self.bidder)
		return word

	@models.permalink
	def get_absolute_url(self):
		return ('bid:detail',(), { 'pk':self.pk })

class BidChosen(models.Model):
	"""docstring for BidChosen"""
	bid = models.ForeignKey(Bid)
	date_chosen = models.DateTimeField(auto_now_add=True, editable=False)

	def __unicode__(self):
			return self.bid
'''
#### new bid objects		
class BidOpen(models.Model):
	unique_id = models.CharField(max_length=100, unique=True)
	job = models.OneToOneField(Job)
	is_done = models.BooleanField(default=False)
	bid_open = models.DateTimeField(auto_add_now=True)
	bid_close = models.DateField()

	def __unicode__(self):
		return self.unique_id

	def save(self, *args, **kwargs):
		super(BidOpen, self).save(*args, **kwargs)
		if not self.unique_id:
			words =str(self.id) + " " + self.job
			self.unique_id = slugify(words)
			self.save()


class BidPost(models.Model):
	person = models.ForeignKey(person)
	unique_id = models.CharField(max_length=100, unique=True)
	bid = models.ForeignKey(BidOpen)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	is_chosen = models.BooleanField(default=False)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.unique_id

	def save(self, *args, **kwargs):
		super(BidOpen, self).save(*args, **kwargs)
		if not self.unique_id:
			words =str(self.id) + " " + self.job
			self.unique_id = slugify(words)
			self.save()

'''