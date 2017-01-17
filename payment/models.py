from django.db import models

class PaymentType(models.Model):
	payment_type = models.CharField(max_length=200)
	info = models.TextField()
	slug = models.SlugField(max_length=200, unique=True)

	def __unicode__(self):
		return self.payment_type


