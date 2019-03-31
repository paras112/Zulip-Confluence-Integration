from django.db import models

# Create your models here.
class ConfluenceData(models.Model):
	data=models.IntegerField(default=0)

	def __unicode__(self):
		return self.data