from django.contrib import admin
from django.contrib.sites.models import RequestSite
from applications.models import App, Data,  IORegistry, Domain
from notifications import notify

def make_active(modeladmin, request, queryset):
	print queryset
	queryset.update(is_active=True)
	for app in queryset:
		notify.send(request.user, recipient=app.author, verb='app_activated' , description = app.name )
make_active.short_description = "Activate selected apps"

class AppAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'responsibility', 'is_active','source_code_host']
    ordering = ['name']
    actions = [make_active]


admin.site.register(App , AppAdmin)
admin.site.register(Data)
admin.site.register(IORegistry)
admin.site.register(Domain)
