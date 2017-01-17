from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from PIL import Image
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

CHOICES = (
	('doer','doer'),
	('poster','poster'),
	)
class PersonClassification(models.Model):
	person_class = models.CharField(max_length=200)
	description  = models.TextField()
	slug 		 = models.SlugField(unique=True, max_length=100)

	def __unicode__ (self):
		return self.person_class

class PersonSkills(models.Model):
	skill = models.CharField(max_length=50)
	description = models.TextField()
	slug  = models.SlugField(unique=True, max_length=50)

	def __unicode__ (self):
		return self.skill

class PersonBadge(models.Model):
	"""docstring for PersonBadges"""

	badge = models.CharField(max_length=50)
	description = models.TextField()
	slug = models.SlugField(unique=True, max_length=50)
	image = models.ImageField(upload_to="media/images/badges", blank=True)

	def __unicode__(self):
		return self.badge

class Person(models.Model):
	person 			= models.OneToOneField(User)
	person_class 	= models.ForeignKey('PersonClassification')
	is_verified  	= models.BooleanField(default=False)
	is_active	 	= models.BooleanField(default=False)
	address		 	= models.TextField()
	info		 	= models.TextField(blank=True)
	birthday	 	= models.DateField()
	firstname	 	= models.CharField(max_length=100)
	lastname 	 	= models.CharField(max_length=100)
	created_at 	 	= models.DateTimeField(auto_now_add=True, editable=False)
	slug 		 	= models.SlugField(unique=True, max_length=100, default='')
	#image 		 	= models.ImageField(upload_to="media/images", blank=True, 
	#									default='media/images/default.jpg')
	contactno	 	= models.CharField(max_length=100)
	#classification 	= models.CharField(choices=CHOICES,max_length=10)
	skills 			= models.ManyToManyField(PersonSkills,blank=True)
	badge 			= models.ManyToManyField(PersonBadge, blank=True)
	image_thumbs = ImageSpecField(source='image',
                                      processors=[ResizeToFill(150, 150)],
                                      format='JPEG',
                                      options={'quality': 50},)
	image = ProcessedImageField(upload_to="media/images",
                                           processors=[ResizeToFill(150, 150)],
                                           format='JPEG',
                                           options={'quality': 75})

	
	def __unicode__(self):
		name = self.firstname + " " + self.lastname
		return name

	def save(self, *args, **kwargs):
		super(Person, self).save(*args, **kwargs)
		if not self.slug:
			words =str(self.id)+" "+self.firstname
			self.slug = slugify(words)
			#image =  self.image
			#self.image_thumbnail = image.thumbnail((200,200), Image.ANTIALIAS)
			self.save()


	@models.permalink
	def get_absolute_url(self):
		return ('person:detail',(), {'slug':self.slug})

