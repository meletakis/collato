from tastypie.authorization import Authorization
import copy
from tastypie.resources import ModelResource, ALL, Resource
from tastypie import fields
from django.contrib.auth.models import User

from roleapp.models import Role
from userprofiles.models import UserProfile
from relationships.models import RelationshipStatus, Relationship
from actstream.models import Action as activities
from notifications.models import Notification as notifications
from applications.models import Action as appaction
from applications.models import App, Data
from responsibilities.models import Responsibility, Assignment
from django.contrib.contenttypes.models import ContentType
import random


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization= Authorization()
        filtering = {
		'is_superuser' : ALL,
		'username' : ALL,
		}


class RoleTypeResource(ModelResource):
    class Meta:
        queryset = Role.objects.all()
        resource_name = 'role'
        allowed_methods = ['get','post']
        
        excludes = [] # poia na min emfanizei
        #fields = ['id'] # poia na emfanizei
        include_resource_uri = False
        authorization= Authorization()
        filtering = {
			'type' : ALL
			}
			#http://127.0.0.1:8000/api/roles/list/?type__startswith=M returns "Maintainers"

        
    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['roles'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
        return data_dict
        
        
class UserProfileResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	role = fields.ForeignKey(RoleTypeResource, 'role')
	
	class Meta:
		queryset = UserProfile.objects.all()
		resource_name = 'profile'
		excludes = [] # poia na min emfanizei
		#fields = ['id'] # poia na emfanizei
		filtering = {
			'user' : ALL
			}
		include_resource_uri = False
		authorization= Authorization()
			#http://127.0.0.1:8000/api/roles/list/?type__startswith=M returns "Maintainers"


	def alter_list_data_to_serialize(self, request, data_dict):
		if isinstance(data_dict, dict):
			if 'meta' in data_dict:
				# Get rid of the "meta".
				del(data_dict['meta'])
				# Rename the objects.
				data_dict['users'] = copy.copy(data_dict['objects'])
				del(data_dict['objects'])
		return data_dict
		


class RelationshipStatusResource(ModelResource):
	from_role = fields.ForeignKey(RoleTypeResource, 'from_role', null=True)
	to_role = fields.ForeignKey(RoleTypeResource, 'to_role', null=True)
	class Meta:
		queryset = RelationshipStatus.objects.all()
		resource_name = 'relationship_status'
		authorization= Authorization()
        
class RelationshipResource(ModelResource):
	from_user = fields.ForeignKey(UserResource, 'from_user')
	to_user = fields.ForeignKey(UserResource, 'to_user')
	status = fields.ForeignKey(RelationshipStatusResource, 'status')

	class Meta:
		queryset = Relationship.objects.all()
		resource_name = 'relationship'
		authorization= Authorization()
		

class AppDataResource(ModelResource):
	class Meta:
		allowed_methods = ['get']
		queryset = Data.objects.all()
		resource_name = 'app_data'
		authorization= Authorization()

class AppResource(ModelResource):
	class Meta:
		allowed_methods = ['get']
		queryset = App.objects.all()
		resource_name = 'apps'
		authorization= Authorization() 
		
class ContentTypeResource(ModelResource):
	class Meta:
		allowed_methods = ['get']
		queryset = ContentType.objects.all()
		resource_name = 'content_type'
		authorization= Authorization()  
		
class AppStreamResource(ModelResource):	
	actor_content_type = fields.ForeignKey(ContentTypeResource, 'actor_content_type')
	target_content_type = fields.ForeignKey(ContentTypeResource, 'target_content_type')
	action_object_content_type = fields.ForeignKey(ContentTypeResource, 'action_object_content_type')

	class Meta:
		filtering = {
		'action_object_object_id' : ALL,
		'actor_object_id' : ALL,
		'data' : ALL,
		'target_object_id' : ALL,
		'description' : ALL,
		'verb' : ALL,
		'timestamp': ['exact', 'lt', 'lte', 'gte', 'gt']
		}		
		queryset = appaction.objects.all()
		resource_name = 'app_activities'
		allowed_methods = ['get','post','put','patch']
		authorization= Authorization()
		include_resource_uri = False		
		
class ActionStreamResource(ModelResource):
	actor_content_type = fields.ForeignKey(ContentTypeResource, 'actor_content_type')
	target_content_type = fields.ForeignKey(ContentTypeResource, 'target_content_type')
	action_object_content_type = fields.ForeignKey(ContentTypeResource, 'action_object_content_type')
	
	class Meta:
		queryset = activities.objects.all()
		resource_name = 'activities'
		allowed_methods = ['get','post',]
		authorization= Authorization()


class NotificationsResource(ModelResource):

	# the two above fields can be null
	action_object_content_type = fields.ToOneField('resources.ContentTypeResource', attribute = 'action_object_content_type', related_name='action_object_content_type', full=True, null=True)
	target_content_type = fields.ToOneField('resources.ContentTypeResource', attribute = 'target_content_type', related_name='target_content_type', full=True, null=True)
	actor_content_type = fields.ForeignKey(ContentTypeResource, 'actor_content_type')
	recipient = fields.ForeignKey(UserResource, 'recipient')
	#target_content_type = fields.ForeignKey(ContentTypeResource, 'target_content_type')
	#action_object_content_type = fields.ForeignKey(ContentTypeResource, 'action_object_content_type')
	
	class Meta:
		queryset = notifications.objects.all()
		resource_name = 'notifications'
		allowed_methods = ['get','post',]
		authorization= Authorization() 
		include_resource_uri = False     

class Ethesis_confirmation_Resource(ModelResource):

	class Meta:
		queryset = User.objects.all()
		allowed_methods = ['get']
		authorization= Authorization()
		resource_name = 'ethesis_confirmation'
		filtering = {
			'id' : ALL
			}
		fields = ['id','username']


	def dehydrate(self, bundle):
	    bundle.data['ethesis_confirmation'] = random.choice(['not submitted', 'submitted', 'accepted'])
	    return bundle
	    
class Owed_courses_Resource(ModelResource):

	class Meta:
		queryset = User.objects.all()
		allowed_methods = ['get']
		authorization= Authorization()
		resource_name = 'owed_courses'
		filtering = {
			'id' : ALL
			}
		fields = ['id','username']


	def dehydrate(self, bundle):
	    bundle.data['owed_courses'] = random.choice(['0', '2', '4'])
	    return bundle


