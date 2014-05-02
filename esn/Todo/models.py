from django.db import models
from django.utils.translation import ugettext as _

class TodoList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField( _("Name"), max_length=255, unique= True,blank=False, null= False)
    source_code_host = models.URLField( _("Source Code Host"), unique= False,blank=False, null= False)
    description = models.TextField ( _("Description"), unique= False , blank=False, null= False)
    def __unicode__(self):
        return self.name



class TodoItem(models.Model):
    DATA_TYPE_CHOICES = (
    ("User_Input", _("User_Input")),
    ("Profile_Input", _("Profile_Input")),
    ("Application_Input", _("Application_Input")),
    ("Output", _("Output")), )
        
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(TodoList)
    name = models.CharField(_("Name"),max_length=100, unique= False,blank=False, null= False)
    description = models.TextField ( _("Description"), unique= False , blank=False, null= False)
    data_type = models.CharField(_("Data Type"),max_length=50, blank=False, null= False, choices=DATA_TYPE_CHOICES,default= None)
    expiration_period = models.IntegerField(null= True, blank=True,)
    required = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name
