from django.shortcuts import render_to_response, get_object_or_404, render
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from django.core.validators import URLValidator
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from responsibilities.models import Responsibility
from django import forms
from jsonfield import JSONField
from django.contrib.auth.models import User

try:
    from django.utils import timezone
    now = timezone.now
except ImportError:
    from datetime import datetime
    now = datetime.now

from applications import settings as app_settings
from applications.signals import action
from applications.compat import get_user_model
from applications.actions import action_handler
from django.utils.translation import ugettext as _


User = get_user_model()


class Domain (models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField( _("Name") ,max_length=50, unique= True,blank=False, null= False, )
    Description = models.CharField ( _("Description"), max_length=512, unique= False , blank=False, null= False,)
    def __unicode__(self):
        return self.Name


class App(models.Model):
    
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User) 
    name = models.CharField( _("Name"), max_length=255, unique= True,blank=False, null= False)
    responsibility = models.ForeignKey(Responsibility, verbose_name=_('responsibility'))
    source_code_host = models.URLField( _("Source Code Host"), unique= False,blank=False, null= False)
    description = models.TextField ( _("Description"), unique= False , blank=False, null= False)
    domain = models.ForeignKey(Domain,blank=False, null=False, verbose_name=_('Domain'))
    is_active = models.BooleanField(_('active'), default=False, )
    def __unicode__(self):
        return self.name

    def get_json(self):
        return {
            'id': self.id, 
            'name': self.name,
            'description' : self.description,
            'domain' : self.domain.id,
            'responsibility' : self.responsibility.Name,
            'active' : self.is_active,
            'author' : self.author.username  }

    
class Data(models.Model):
    
    DATA_TYPE_CHOICES = (
    ("User_Input", _("User_Input")),
    ("Profile_Input", _("Profile_Input")),
    ("Application_Input", _("Application_Input")),
    ("Output", _("Output")), )

    id = models.AutoField(primary_key=True)
    name = models.CharField(_("Name"),max_length=100, unique= False,blank=False, null= False)
    slug =models.SlugField(_("Slug") ,max_length=100, unique=False, blank=False, null= False )
    description = models.TextField ( _("Description"), unique= False , blank=False, null= False)
    data_type = models.CharField(_("Data Type"),max_length=50, blank=False, null= False, choices=DATA_TYPE_CHOICES,default= None)
    expiration_period = models.IntegerField(null= True, blank=True,)
    required = models.BooleanField(default=True)
    domain = models.ForeignKey(Domain,blank=False, null=False, verbose_name=_('Domain'))
    semantics = JSONField()


    def __unicode__(self):
        return self.name

    def get_json(self):
        return {
            'id': self.id, 
            'name': self.name,
            'description' : self.description,
            'domain' : self.domain.id ,
            'slug' : self.slug }

    def get_json_for_visualization(self):
        IORegistry_info = IORegistry.objects.get(data_id = self.id)
        print data_info
        return {
            'id': self.id, 
            'app': self.app.name,
            'data_id' : self.data.id,
            'type' : self.data_type, 
            'idle': self.idle,
            'name' : data_info.name,
            'description' : data_info.description,
            'domain' :  data_info.domain.id,
            'author' : app_info.author.username, } 


class IORegistry(models.Model):


    DATA_TYPE_CHOICES = (
    ("Input", "Input"),
    ("Output", "Output"), )
    
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(App)
    data = models.ForeignKey(Data)
    data_type= models.CharField(max_length=50,blank=False, null= False, choices=DATA_TYPE_CHOICES,default= None)
    idle = models.BooleanField(default=False)     

    def get_json(self):
        data_info =  Data.objects.get(id = self.data.id)
        app_info = App.objects.get(id = self.app.id)
        print data_info
        return {
            'id': self.id, 
            'app': self.app.name,
            'data_id' : self.data.id,
            'type' : self.data_type, 
            'idle': self.idle,
            'name' : data_info.name,
            'description' : data_info.description,
            'domain' :  data_info.domain.id,
            'author' : app_info.author.username, }

    def get_json_for_visualization(self):
        data_info =  Data.objects.get(id = self.data.id)
        app_info = App.objects.get(id = self.app.id)
        print data_info
        return {
            'id': self.id, 
            'app': self.app.name,
            'data_id' : self.data.id,
            'type' : self.data_type, 
            'idle': self.idle,
            'name' : data_info.name,
            'description' : data_info.description,
            'domain' :  data_info.domain.id,
            'author' : app_info.author.username, }            

class Action(models.Model):
    """
    Action model describing the actor acting out a verb (on an optional
    target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>

    Examples::

        <justquick> <reached level 60> <1 minute ago>
        <brosner> <commented on> <pinax/pinax> <2 hours ago>
        <washingtontimes> <started follow> <justquick> <8 minutes ago>
        <mitsuhiko> <closed> <issue 70> on <mitsuhiko/flask> <about 2 hours ago>

    Unicode Representation::

        justquick reached level 60 1 minute ago
        mitsuhiko closed issue 70 on mitsuhiko/flask 3 hours ago

    HTML Representation::

        <a href="http://oebfare.com/">brosner</a> commented on <a href="http://github.com/pinax/pinax">pinax/pinax</a> 2 hours ago

    """
    actor_content_type = models.ForeignKey(ContentType, related_name='app_actor')
    actor_object_id = models.CharField(max_length=255)
    actor = generic.GenericForeignKey('app_actor_content_type', 'app_actor_object_id')

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(ContentType, related_name='app_target',
        blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type',
        'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType,
        related_name='app_action_object', blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True,
        null=True)
    action_object = generic.GenericForeignKey('action_object_content_type',
        'action_object_object_id')

    timestamp = models.DateTimeField(default=now)

    public = models.BooleanField(default=True)

    objects = app_settings.get_action_manager()

    class Meta:
        ordering = ('-timestamp', )

    def __unicode__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.target:
            if self.action_object:
                return _('%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago') % ctx
            return _('%(actor)s %(verb)s %(target)s %(timesince)s ago') % ctx
        if self.action_object:
            return _('%(actor)s %(verb)s %(action_object)s %(timesince)s ago') % ctx
        return _('%(actor)s %(verb)s %(timesince)s ago') % ctx

    def actor_url(self):
        """
        Returns the URL to the ``actstream_actor`` view for the current actor.
        """
        return reverse('app_actor', None,
                       (self.actor_content_type.pk, self.actor_object_id))

    def target_url(self):
        """
        Returns the URL to the ``actstream_actor`` view for the current target.
        """
        return reverse('app_actor', None,
                       (self.target_content_type.pk, self.target_object_id))

    def action_object_url(self):
        """
        Returns the URL to the ``actstream_action_object`` view for the current action object
        """
        return reverse('app_actor', None,
            (self.action_object_content_type.pk, self.action_object_object_id))

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @models.permalink
    def get_absolute_url(self):
        return ('app.views.detail', [self.pk])


# convenient accessors
actor_stream = Action.objects.actor
action_object_stream = Action.objects.action_object
target_stream = Action.objects.target
user_stream = Action.objects.user
model_stream = Action.objects.model_actions




if app_settings.USE_JSONFIELD:
    try:
        from jsonfield.fields import JSONField
    except ImportError:
        raise ImproperlyConfigured('You must have django-jsonfield installed '
                                'if you wish to use a JSONField on your actions')
    JSONField(blank=True, null=True).contribute_to_class(Action, 'data')

# connect the signal
action.connect(action_handler, dispatch_uid='app.models')
