# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from applications import views


urlpatterns = patterns('applications',
    url(r'^$', view=login_required (views.index)),
    url(r'^new/', view=login_required (views.new_app2) ),
    url(r'^remove/', view=login_required (views.remove) ),
    url(r'^remove_app/(?P<app_id>\d+)/$', view=login_required (views.remove_specific_app )),    
    url(r'^edit/', view=login_required (views.edit) ),
    url(r'^edit_app/(?P<app_id>\d+)/$', view=login_required (views.edit_specific_app) ),
    url(r'^visuzalize_app/(?P<app_id>\d+)/$', view=login_required (views.visualize_specific_app) ),
    url(r'^run/', view=login_required (views.run) ),
    url(r'^visualize/', view=login_required (views.visualize) ),
    url(r'^domain/new/', view=login_required (views.new_domain) ),
    url(r'thanks$', view=login_required (TemplateView.as_view(template_name='app/thanks.html') ), name="thanks"),
)
