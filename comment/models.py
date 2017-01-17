from django.db import models
from person.models import Person
from job.models import Job 
CHOICES = (
	(1,'poor'),
	(2,'ok'),
	(3,'average'),
	(4,'good'),
	(5,'best'),
	)
class Comment(models.Model):
	commentor = models.ForeignKey(Person, related_name='commentor')
	receiver = models.ForeignKey(Person, related_name='receiver')
	job = models.ForeignKey(Job)
	rating = models.IntegerField(choices=CHOICES,max_length=6)
	comment = models.TextField()
	date_time_posted = models.DateTimeField(auto_now_add=True, editable=False)

	def __unicode__(self):
		return self.comment

	class Meta:
		ordering=['receiver','-date_time_posted', ]