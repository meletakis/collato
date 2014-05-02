from django.contrib import admin
from django.contrib.sites.models import RequestSite
from roleapp.models import Role

class RoleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'id', 'type', 'desc', )
    list_editable = ('id', 'type', 'desc', )

admin.site.register(Role,RoleAdmin)
