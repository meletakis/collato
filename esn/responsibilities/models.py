from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Responsibility(models.Model):
	
	id = models.AutoField(primary_key=True)
	Name = models.CharField(max_length=255, unique= True,blank=False, null= False)
	description = models.CharField(max_length=1024,blank=False, null= False)
	def __unicode__(self):
		return self.Name

class Assignment(models.Model):
	Responsibility = models.ForeignKey('Responsibility')
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	responsible = generic.GenericForeignKey('content_type', 'object_id')
	def __unicode__(self):
		return self.Responsibility.Name