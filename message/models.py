from django.db import models
from person.models import Person 
from django.template.defaultfilters import slugify

class Message(models.Model):
	title = models.CharField(max_length=250)
	content = models.TextField()
	receiver = models.ForeignKey(Person)
	is_read = models.BooleanField(default=False)
	slug = models.SlugField(blank=True)
	pub_date_time = models.DateTimeField(auto_now_add=True, editable=False)
	sender = models.ForeignKey(Person, related_name="sender", blank=True)

	class Meta:
		ordering=['-pub_date_time']
	
	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Message, self).save(*args, **kwargs)
		if not self.slug:
			words =self.title+" "+str(self.id)
			self.slug = slugify(words)
			self.save()

	@models.permalink
	def get_absolute_url(self):
		return ('message:detail',(), {'slug':self.slug})