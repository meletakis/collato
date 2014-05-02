try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns

from Todo import views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('Todo.views',
    url(r'^$', view=login_required (views.index)),
)
