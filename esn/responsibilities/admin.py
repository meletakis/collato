from django.contrib import admin
from django.contrib.sites.models import RequestSite
from responsibilities.models import Responsibility, Assignment

class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'id', 'Name', 'description', )
    list_editable = ('id', 'Name', 'description', )

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'Responsibility', 'content_type', 'object_id', 'responsible')
    list_editable = ( 'Responsibility',  'content_type', 'object_id',)   

admin.site.register(Responsibility,ResponsibilityAdmin)
admin.site.register(Assignment, AssignmentAdmin)

