from django.db import models
from person.models import Person
from job.models import Job

class Discussion(models.Model):
	"""docstring for Discussion"""
	person = models.ForeignKey(Person)
	job = models.ForeignKey(Job)
	pub_date = models.DateTimeField(auto_now_add=True, editable=False)
	message = models.TextField()

	def __unicode__(self):
		person_job = str(self.person) + " " + str(self.job)
		return person_job

	class Meta:
		ordering=['-pub_date', ]