from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from applications.forms import AppForm, DataApplicationForm, DomainForm, DataApplicationForm2, AppForm2
from applications.models import App, Data, IORegistry, Domain, IORegistry
from userprofiles.models import UserProfile
from django.contrib.contenttypes.models import ContentType
from responsibilities.models import Responsibility, Assignment
from roleapp.models import Role
from django.contrib.auth.models import User
from django.utils import simplejson
from userprofiles.models import UserProfile
from django.db.models import Q
from notifications import notify
import simplejson
import json
from django.forms.models import modelformset_factory
from relationships.models import RelationshipStatus
from actstream import actions, models, compat, action

def index(request):
    
    if str(request.user.profile.role) == "Developer":
        return render(request, 'app/developer.html',)
    else: 
        user = UserProfile.objects.get( user_id = request.user.id )
        role_ct = ContentType.objects.get(app_label="roleapp", model="role")
        user_ct = ContentType.objects.get(app_label="auth", model="user")

        try:
            user_assigments = Assignment.objects.get(content_type_id = role_ct, object_id = user.role_id )
            apps = App.objects.filter(responsibility_id = user_assigments.Responsibility_id, is_active = True )
        except Exception, e:
            apps = []
        else:
            pass

        try:
            print "pray"
            user_assigments = Assignment.objects.get(content_type_id = user_ct, object_id = request.user.id )
            print user_assigments
            apps += App.objects.filter(responsibility_id = user_assigments.Responsibility_id , is_active = True )
        except Exception, e:
            pass
        else:
            pass

        return render(request, 'app.html', {'apps' : apps })


def new_app(request):

    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    App_Data_FormSet = formset_factory(DataApplicationForm, max_num=10, formset=RequiredFormSet)
    app_data = IORegistry.objects.all().filter(data_type = "Output").values_list( 'data')
    print app_data
    #profile_data = UserProfile.objects.all().values_list('aboutMe', 'displayName', 'email')
    profile_data = UserProfile._meta.get_all_field_names()
    #print profile_data
    #print type (profile_data)

    #check for developer Role
    if str(request.user.profile.role) != "Developer":
        return HttpResponseRedirect('/')
    

    if request.method == 'POST': # If the form has been submitted...
        app_form = AppForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        app_data_formset = App_Data_FormSet(request.POST, request.FILES)
        print "IN POST"
        
        if app_form.is_valid() and app_data_formset.is_valid():
            app_name = app_form.cleaned_data['name']
            source = app_form.cleaned_data['source_code_host']
            resp = app_form.cleaned_data['responsibility']
            desc = app_form.cleaned_data['description']
            domain = app_form.cleaned_data['domain']
            app_obj = App(name=app_name, author=request.user, source_code_host=source, responsibility = resp, description = desc, domain = domain)
            app_obj.save()
            app_obj.Source_code_host = source+'?app_id='+str(app_obj.id)
            app_obj.save()
            
            for form in app_data_formset.forms:
                data_name = form.cleaned_data['name']
                dat_type = form.cleaned_data['data_type']
                domain = form.cleaned_data['domain']
                description = form.cleaned_data['description']
                data_obj = Data ( app = app_obj, name = data_name, data_type = dat_type, domain = domain , description = description)
                data_obj.save()

                if ( dat_type == "Output"):
                    ioregistry_obj = IORegistry ( app = app_obj , data = data_obj, data_type = dat_type)
                    print ioregistry_obj
                    ioregistry_obj.save()
                else:
                    ioregistry_obj = IORegistry ( app = app_obj , data = data_obj, data_type = "Input")
                    print ioregistry_obj
                    ioregistry_obj.save()


            return HttpResponseRedirect('/apps/') # Redirect to a 'success' page
        else:
            print "FORM VALIDATION ERROR"
            print app_form.errors
            print app_data_formset.errors
    else:
        app_form = AppForm()
        app_data_formset = App_Data_FormSet()
    
    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'app_form': app_form,
         'app_data_formset': app_data_formset,
         'app_data' : simplejson.dumps(list(app_data)),
         'profile_data' : simplejson.dumps(list(profile_data)),
        }
    c.update(csrf(request))
    
    return render_to_response('app/developer/index.html', c, context_instance=RequestContext(request))


def edit(request):

    if str(request.user.profile.role) != "Developer":
        return HttpResponseRedirect('/')
    else:
    	apps_id = set()
        apps = App.objects.filter(author = request.user ) #take all users applications
        for app in apps: #find apps that they DONT have idle inputs and remove them from queyset
        	if  not ( IORegistry.objects.filter( app_id = app.id  , idle = True ).count() == 0): 
        		apps_id.add(app.id )
        		
        apps = App.objects.filter(pk__in = apps_id)
        return render_to_response('app/developer/edit.html', {'apps' : apps },context_instance=RequestContext(request))

def run(request):
    if str(request.user.profile.role) != "Developer":
        return HttpResponseRedirect('/')
    else:
        apps_created= App.objects.filter(author = request.user )
        
        user = UserProfile.objects.get( user_id = request.user.id )
        role_ct = ContentType.objects.get(app_label="roleapp", model="role")
        user_ct = ContentType.objects.get(app_label="auth", model="user")

        try:
            user_assigments = Assignment.objects.get(content_type_id = role_ct, object_id = user.role_id )
            apps = App.objects.filter(responsibility_id = user_assigments.Responsibility_id , is_active = True )
        except Exception, e:
            apps = []
        else:
            pass

        try:
            print "pray"
            user_assigments = Assignment.objects.get(content_type_id = user_ct, object_id = request.user.id )
            print user_assigments
            apps += App.objects.filter(responsibility_id = user_assigments.Responsibility_id , is_active = True)
        except Exception, e:
            pass
        else:
            pass
        
        return render_to_response('app/developer/run.html', {'apps_created':apps_created,'apps':apps }, context_instance=RequestContext(request))


    
def new_domain(request):
    if request.method == 'POST': # If the form has been submitted...
        domain_form = DomainForm(request.POST) # A form bound to the POST data
        
        if domain_form.is_valid():
            domain_name = domain_form.cleaned_data['Name']
            desc = domain_form.cleaned_data['Description']
            domain_obj = Domain(Name=domain_name, Description = desc, )
            domain_obj.save()
            return HttpResponseRedirect('/apps/') # Redirect to a 'success' page
        else:
            print "FORM VALIDATION ERROR"
            return HttpResponseRedirect('/apps/domain/new')

    else:
        domain_form = DomainForm()
    
    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'domain_form': domain_form,
        }
    c.update(csrf(request))
    
    return render_to_response('app/developer/domain.html', c, context_instance=RequestContext(request))
                                            



def remove(request):
    if str(request.user.profile.role) != "Developer":
        return HttpResponseRedirect('/')
    else:
        apps_created= App.objects.filter(author = request.user )
                
    return render_to_response('app/developer/remove.html', {'apps_created':apps_created, }, context_instance=RequestContext(request))



def remove_specific_app(request,app_id):

    app_name = App.objects.get(pk = app_id ).name
    ioregistry_inputs = IORegistry.objects.filter( app_id = app_id, data_type = "Input" )
    for ioregistry_input in ioregistry_inputs:
    	if (IORegistry.objects.filter( data_id = ioregistry_input.data_id).count() <= 1 ):
    		Data.objects.filter(pk = ioregistry_input.data_id ).delete()
    	IORegistry.objects.filter( pk = ioregistry_input.id).delete()


    ioregistry_outputs = IORegistry.objects.filter( app_id = app_id, data_type = "Output" )
    for ioregistry_output in ioregistry_outputs:
    	if (IORegistry.objects.filter( data_id = ioregistry_output.data_id).count() == 1 ): #if exist only one row with this data delete it
    		IORegistry.objects.filter( pk = ioregistry_output.id).delete()
    		Data.objects.filter(pk = ioregistry_output.data_id ).delete()

    	elif ( IORegistry.objects.filter( data_id = ioregistry_output.data_id,  data_type = "Input").count() >= 1 ):
    		idle_inputs = IORegistry.objects.filter( data_id = ioregistry_output.data_id,  data_type = "Input")
    		for idle_input in idle_inputs:
    			p = IORegistry.objects.get(pk=idle_input.id)
    			p.idle = True #update idle value to true
    			p.save()
    		IORegistry.objects.filter( pk = ioregistry_output.id).delete()

    App.objects.filter(pk = app_id ).delete()

    viewer = request.user
    owner_user = request.user
    owner_user_role = UserProfile.objects.get( user_id = owner_user.id )

    if  (RelationshipStatus.objects.all().filter (to_role_id = owner_user_role.role_id).count() == 0 ):
        print " No relationship found "
        if  (RelationshipStatus.objects.all().filter (to_role_id__isnull=True ).count() >= 0 ):
            for relationship in RelationshipStatus.objects.all().filter (to_role_id__isnull=True):
                action.send(request.user, verb='posted', action_object = owner_user, target=relationship,  post_content="I have just deleted application <i>"+app_name+"</i>")
    else:
        for relationship in RelationshipStatus.objects.all().filter (to_role_id = owner_user_role.role_id):
            action.send(request.user, verb='posted', action_object = owner_user, target=relationship,  post_content="I have just deleted application <i>"+app_name+"</i>") # action creation
        if  (RelationshipStatus.objects.all().filter (to_role_id__isnull=True ).count() >= 0 ):
            for relationship in RelationshipStatus.objects.all().filter (to_role_id__isnull=True):
                action.send(request.user, verb='posted', action_object = owner_user, target=relationship,  post_content="I have just deleted the application <i>"+app_name+"</i>")


    return HttpResponseRedirect('/apps/remove/') 








def new_app2(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    DataApplicationFormSet = formset_factory(DataApplicationForm2, max_num=10, formset=RequiredFormSet)

    distinct_application_outputs_objects = set()
    distinct_idle_application_inputs_objects = set()
    all_data = Data.objects.all()
    for data in all_data:
        print data
        if ( IORegistry.objects.all().filter( data_id = data.id , data_type = "Output" ).count() > 0  ): # if exist output data
            distinct_application_outputs_objects.add(data.id)

        elif ( IORegistry.objects.all().filter( data_id = data.id , idle = True ).count() > 0  ):
            distinct_idle_application_inputs_objects.add(data.id)


    idle_application_inputs = [a.get_json() for a in   Data.objects.filter(pk__in = distinct_idle_application_inputs_objects) ] 
    application_outputs = [a.get_json() for a  in  Data.objects.filter(pk__in = distinct_application_outputs_objects )] 
    user_inputs = [a.get_json() for a  in  Data.objects.filter(data_type = "User" )] 
    profile_data = UserProfile._meta.get_all_field_names()


    if request.method == 'POST': # If form has been submitted...
        main_form = AppForm2(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        formset = DataApplicationFormSet(request.POST, request.FILES)

        if main_form.is_valid() and formset.is_valid():
            owner_user = request.user
            owner_user_role = UserProfile.objects.get( user_id = owner_user.id )
            app_name = main_form.cleaned_data['name']
            source = main_form.cleaned_data['source_code_host']
            resp = main_form.cleaned_data['responsibility']
            desc = main_form.cleaned_data['description']
            domain = main_form.cleaned_data['domain']
            app_obj = App(name=app_name, author=request.user, source_code_host=source, responsibility = resp, description = desc, domain = domain)
            app_obj.save()
            app_obj.source_code_host = source+'?app_id='+str(app_obj.id)
            app_obj.save()

            s_admins = User.objects.filter(is_superuser = 1)
            for s_admin in s_admins:
                notify.send(request.user, recipient=s_admin, verb='created_new_app' , description = app_name )
            
            for form in formset.forms:
                data_name = form.cleaned_data['name']
                dat_type = form.cleaned_data['data_type']
                domain = form.cleaned_data['domain']
                description = form.cleaned_data['description']
                slug = form.cleaned_data['slug']


                
                if ( dat_type == "User_Input"):
                    dat_type_flag = "User"
                elif( dat_type == "Profile_Input"):
                    dat_type_flag = "Profile"
                else:
                    dat_type_flag = "App"

                #counter for data with given data
                num_results = Data.objects.filter(name = data_name, data_type = dat_type_flag, domain = domain , description = description  ).count()

                # find if data already exist

                if ( num_results == 0): # if data does not exist create it
                    data_obj = Data ( name = data_name, data_type = dat_type_flag, domain = domain , description = description , slug = slug )
                    data_obj.save()
                else:       #if data exist give the value to data_obj
                    data_obj = Data.objects.get(name = data_name, data_type = dat_type_flag, domain = domain , description = description  )

                if ( dat_type == "Output"):
                    ioregistry_obj = IORegistry ( app = app_obj , data = data_obj, data_type = dat_type)
                    # save ioregistry object
                    ioregistry_obj.save()

                    #check if this data exist as idle input
                    if ( IORegistry.objects.filter(data = data_obj, idle = True  ).count() > 0 ):
                        # if exist update value as Not idle (because its an output) nad notify user
                        idle_objects = IORegistry.objects.filter(data = data_obj, idle = True  )
                        for idle_object in idle_objects:
                            idle_object.idle = False
                            idle_object.save()
                            app = App.objects.get ( id = idle_object.app.id )
                            print app
                            notify.send(request.user, recipient=app.author, verb='created_idle_input' , description = data_obj.name)


                else:
                    # if data is Application input and it does not exist idle = true
                    if ( num_results == 0 and dat_type == "Application_Input"):
                        idle = True
                    else:
                        idle = False

                    ioregistry_obj = IORegistry ( app = app_obj , data = data_obj, data_type = "Input", idle = idle)
                    print ioregistry_obj
                    ioregistry_obj.save()
                    
            if  (RelationshipStatus.objects.all().filter (to_role_id = owner_user_role.role_id).count() == 0 ):
				print " No relationship found "
				if  (RelationshipStatus.objects.all().filter (to_role_id__isnull=True ).count() >= 0 ):
					for relationship in RelationshipStatus.objects.all().filter (to_role_id__isnull=True):
						action.send(request.user, verb='posted', action_object = owner_user, target=relationship,  post_content="I have just created application <i>"+app_name+"</i>")
            else:
				for relationship in RelationshipStatus.objects.all().filter (to_role_id = owner_user_role.role_id):
					action.send(request.user, verb='posted', action_object = owner_user, target=relationship,  post_content="I have just created application <i>"+app_name+"</i>") # action creation
				if  (RelationshipStatus.objects.all().filter (to_role_id__isnull=True ).count() >= 0 ):
					for relationship in RelationshipStatus.objects.all().filter (to_role_id__isnull=True):
						action.send(request.user, verb='posted', action_object = owner_user, target=relationship,  post_content="I have just created application <i>"+app_name+"</i>")


            return HttpResponseRedirect('/apps/') # Redirect to a 'success' page
    else:
        main_form = AppForm2()
        formset = DataApplicationFormSet()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'main_form': main_form,
         'formset': formset,
         'profile_data' : simplejson.dumps(list(profile_data)),
         'idle_input' : simplejson.dumps(list(idle_application_inputs)),
         'output' : simplejson.dumps(list(application_outputs)),
         'user_inputs' : simplejson.dumps(list(user_inputs)),
        }
    c.update(csrf(request))

    return render_to_response('app/developer/new.html', c, context_instance=RequestContext(request))
    
def edit_specific_app(request,app_id):

	newAdFormSet = modelformset_factory(Data,)

	ioregistry_objects = IORegistry.objects.filter( app_id = app_id , idle = True)
	data_id = set()
	for ioregistry_object in ioregistry_objects:
		print ioregistry_object.data_id
		data_id.add(ioregistry_object.data_id)

	if request.method == 'POST':
	    formset = newAdFormSet(request.POST, request.FILES)
	    if formset.is_valid():
	        formset.save()
	        return render_to_response('conf.html',
	                                 {'state':'Your ad has been successfull created.'},
	                                 context_instance = RequestContext(request),)
	else:
	    formset = newAdFormSet(queryset=Data.objects.filter(pk__in = data_id ))

	return render_to_response('app/developer/edit_app.html',{'formset':formset}, context_instance=RequestContext(request),)


	 
def visualize(request):
    
    if str(request.user.profile.role) == "Developer":
       apps_info = [a.get_json() for a  in   App.objects.all() ]
    else: 
        user = UserProfile.objects.get( user_id = request.user.id )
        role_ct = ContentType.objects.get(app_label="roleapp", model="role")
        user_ct = ContentType.objects.get(app_label="auth", model="user")

        # find apps by role assigment responsibility
        try:
            user_assigments = Assignment.objects.get(content_type_id = role_ct, object_id = user.role_id )
            apps_info = [a.get_json() for a  in App.objects.filter(responsibility_id = user_assigments.Responsibility_id ) ]
        except Exception, e:
            apps = []
        else:
            pass

        # find apps by user assigment responsibility
        try:
            user_assigments = Assignment.objects.get(content_type_id = user_ct, object_id = request.user.id )
            print user_assigments
            apps_info += [a.get_json() for a in App.objects.filter(responsibility_id = user_assigments.Responsibility_id ) ]
        except Exception, e:
            pass
        else:
            pass

    # set apps_id's to a list from json
    apps_id = set()
    for x in range(0, len(apps_info)):
        apps_id.add(apps_info[x]['id'])

    data_json = []
    io_objects = IORegistry.objects.filter(app__in = apps_id ) 
    for  io_object in io_objects:
        print io_object.id


        if (io_object.data_type == "Input" and io_object.idle ): #idle input case
            data =  Data.objects.get( id = io_object.data_id )
            app =  App.objects.get(  id = io_object.app_id )
            data_json += { "from" : "Idle_Application_Input", "to" : app.id, "name" : data.name , "slug" : data.slug },

        elif (io_object.data_type == "Input" ):

            if ( Data.objects.filter( data_type = "User", id = io_object.data_id  ).count() ):
                data =  Data.objects.get(  id = io_object.data_id )
                app =  App.objects.get(  id = io_object.app_id )
                data_json += { "from" : "User_Input", "to" : app.id, "name" : data.name , "slug" : data.slug },
            elif ( Data.objects.filter( data_type = "Profile", id = io_object.data_id  ).count() ):
                data =  Data.objects.get( id = io_object.data_id )
                app =  App.objects.get(  id = io_object.app_id )
                data_json += { "from" : "Profile_Input", "to" : app.id, "name" : data.name , "slug" : data.slug },

            elif ( Data.objects.filter( data_type = "App", id = io_object.data_id  ).count() ):
                if ( IORegistry.objects.filter( data_id = io_object.data_id  , data_type = "Output").count() > 0):
                        data =  Data.objects.get( id = io_object.data_id )
                        app =  App.objects.get(  id = io_object.app_id )
                        outputs = IORegistry.objects.filter( data_id = io_object.data_id  , data_type = "Output") 

                        for output in outputs:
                            output_app =  App.objects.get(  id = output.app_id )
                            data_json += { "from" : output_app.id, "to" : app.id, "name" : data.name , "slug" : data.slug },

        elif (io_object.data_type == "Output" ):

            if ( IORegistry.objects.filter( data_id = io_object.data_id  , data_type = "Input").count() == 0):
                data =  Data.objects.get( id = io_object.data_id )
                app =  App.objects.get(  id = io_object.app_id )
                data_json += { "from" : app.id , "to" : "Idle_Application_Output", "name" : data.name , "slug" : data.slug },             




    return render(request, 'app/visualize.html', {'apps_info' : simplejson.dumps(list(apps_info)) , 'data' : simplejson.dumps(list(data_json)) })


def visualize_specific_app(request, app_id):

    app_name = App.objects.get( id = app_id).name

    '''
    
    if str(request.user.profile.role) == "Developer":
       apps_info = [a.get_json() for a  in   App.objects.all() ]
    else: 
        user = UserProfile.objects.get( user_id = request.user.id )
        role_ct = ContentType.objects.get(app_label="roleapp", model="role")
        user_ct = ContentType.objects.get(app_label="auth", model="user")

        # find apps by role assigment responsibility
        try:
            user_assigments = Assignment.objects.get(content_type_id = role_ct, object_id = user.role_id )
            apps_info = [a.get_json() for a  in App.objects.filter(responsibility_id = user_assigments.Responsibility_id ) ]
        except Exception, e:
            apps_info = []
        else:
            pass

        # find apps by user assigment responsibility
        try:
            user_assigments = Assignment.objects.get(content_type_id = user_ct, object_id = request.user.id )
            print user_assigments
            apps_info += [a.get_json() for a in App.objects.filter(responsibility_id = user_assigments.Responsibility_id ) ]
        except Exception, e:
            pass
        else:
            pass
    '''
    apps_info = [ a.get_json() for a in App.objects.filter(id = app_id) ]

    apps_info = find_apps(apps_info , app_id )

    print "Anadromi returned"
    print apps_info

    # set apps_id's to a list from json
    apps_id = set()
    for x in range(0, len(apps_info)):
        apps_id.add(apps_info[x]['id'])

    data_json = []
    io_objects = IORegistry.objects.filter(app__in = apps_id ) 
    for  io_object in io_objects:
        print io_object.id


        if (io_object.data_type == "Input" and io_object.idle ): #idle input case
            data =  Data.objects.get( id = io_object.data_id )
            app =  App.objects.get(  id = io_object.app_id )
            data_json += { "from" : "Idle_Application_Input", "to" : app.id, "name" : data.name , "slug" : data.slug },

        elif (io_object.data_type == "Input" ):

            if ( Data.objects.filter( data_type = "User", id = io_object.data_id  ).count() ):
                data =  Data.objects.get(  id = io_object.data_id )
                app =  App.objects.get(  id = io_object.app_id )
                data_json += { "from" : "User_Input", "to" : app.id, "name" : data.name , "slug" : data.slug },
            elif ( Data.objects.filter( data_type = "Profile", id = io_object.data_id  ).count() ):
                data =  Data.objects.get( id = io_object.data_id )
                app =  App.objects.get(  id = io_object.app_id )
                data_json += { "from" : "Profile_Input", "to" : app.id, "name" : data.name , "slug" : data.slug },

            elif ( Data.objects.filter( data_type = "App", id = io_object.data_id  ).count() ):
                if ( IORegistry.objects.filter( data_id = io_object.data_id  , data_type = "Output").count() > 0):
                        data =  Data.objects.get( id = io_object.data_id )
                        app =  App.objects.get(  id = io_object.app_id )
                        outputs = IORegistry.objects.filter( data_id = io_object.data_id  , data_type = "Output") 

                        for output in outputs:
                            output_app =  App.objects.get(  id = output.app_id )
                            data_json += { "from" : output_app.id, "to" : app.id, "name" : data.name , "slug" : data.slug },

        elif (io_object.data_type == "Output" ):

            if ( IORegistry.objects.filter( data_id = io_object.data_id  , data_type = "Input").count() == 0):
                data =  Data.objects.get( id = io_object.data_id )
                app =  App.objects.get(  id = io_object.app_id )
                data_json += { "from" : app.id , "to" : "Idle_Application_Output", "name" : data.name , "slug" : data.slug },             




    return render(request, 'app/visualize.html', {'apps_info' : simplejson.dumps(list(apps_info)) , 'data' : simplejson.dumps(list(data_json)) , 'name' : app_name})



def find_apps(apps_info, app_id):

    # for all application outputs find other applications who has these values as inputs and add them to apps_info
    outputs = IORegistry.objects.filter( app_id = app_id , data_type = "Output")
    for output in outputs:
        inputs = IORegistry.objects.filter( data_id = output.data_id , data_type = "Input")

        for input_ob in inputs:
            if  not find_if_app_exist_in_json(apps_info, input_ob.app_id):
				apps_info += [a.get_json() for a in App.objects.filter(id = input_ob.app_id) ]
				find_apps (apps_info, input_ob.app_id )

	# for all application inputs find other applications who has these values as outputs and add them to apps_info				
    inputs = IORegistry.objects.filter( app_id = app_id , data_type = "Input")
    for input_ob in inputs:
        outputs = IORegistry.objects.filter( data_id = input_ob.data_id , data_type = "Output")

        for output in outputs:
            if  not find_if_app_exist_in_json(apps_info, output.app_id):
	            apps_info += [a.get_json() for a in App.objects.filter(id = output.app_id) ]
	            find_apps (apps_info, output.app_id )

    return apps_info

def find_if_app_exist_in_json(apps_info, app_id):

	for x in range(0, len(apps_info)):
		if apps_info[x]['id'] ==  app_id:
			return True

	return False








