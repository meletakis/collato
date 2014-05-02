from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from relationships.forms import RelationshipStatusAdminForm
from relationships.models import Relationship, RelationshipStatus

'''
class RelationshipInline(admin.TabularInline):
    model = Relationship
    raw_id_fields = ('from_user', 'to_user')
    extra = 1
    fk_name = 'from_user'


class UserRelationshipAdmin(UserAdmin):
    inlines = (RelationshipInline,)


class RelationshipStatusAdmin(admin.ModelAdmin):
    form = RelationshipStatusAdminForm
'''
class RelationshipStatusAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'verb','from_role','to_role', 'from_slug', 'to_slug',)
    list_editable = ('name', 'verb', 'from_role','to_role', 'from_slug', 'to_slug',)


admin.site.register(RelationshipStatus, RelationshipStatusAdmin)
