from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import autocomplete_light
autocomplete_light.autodiscover()
admin.autodiscover()

from django.conf.urls.defaults import handler404, handler500

handler404 = 'esn.views.file_not_found_404'
handler500 = 'esn.views.file_not_found_404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'esn.views.home', name='home'),
    # url(r'^esn/', include('esn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.backends.default.urls')),
     (r'^user/', include('userprofiles.urls')),
     (r'^relationships/', include('relationships.urls')),
     (r'^notifications/', include('notifications.urls')),
     (r'^activity/', include('actstream.urls')),
     (r'^todo/', include('Todo.urls')),
     (r'^index/', TemplateView.as_view(template_name="index.html")),
     (r'^$', include('actstream.urls')),
     #(r'^log/', include('registration.auth_urls')),
     #url(r"^account/", include("account.urls")),
     (r'^ajax-upload/', include('cicu.urls')),
     (r'^apps/',include('applications.urls') ),
     (r'^groups/',include('organizations.urls') ),
     (r'^api/', include('api.urls')),
     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
