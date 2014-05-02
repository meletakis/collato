try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns

from actstream import feeds
from actstream import views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('actstream.views',
    # Syndication Feeds
    url(r'^feed/(?P<content_type_id>\d+)/(?P<object_id>\d+)/atom/$',
        feeds.AtomObjectActivityFeed(), name='actstream_object_feed_atom'),
    url(r'^feed/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        feeds.ObjectActivityFeed(), name='actstream_object_feed'),
    url(r'^feed/(?P<content_type_id>\d+)/atom/$',
        feeds.AtomModelActivityFeed(), name='actstream_model_feed_atom'),
    url(r'^feed/(?P<content_type_id>\d+)/(?P<object_id>\d+)/as/$',
        feeds.ActivityStreamsObjectActivityFeed(),
        name='actstream_object_feed_as'),
    url(r'^feed/(?P<content_type_id>\d+)/$',
        feeds.ModelActivityFeed(), name='actstream_model_feed'),
    url(r'^feed/$', feeds.UserActivityFeed(), name='actstream_feed'),
    url(r'^feed/atom/$', feeds.AtomUserActivityFeed(),
        name='actstream_feed_atom'),

    # Follow/Unfollow API
    url(r'^follow/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'follow_unfollow', name='actstream_follow'),
    url(r'^follow_all/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'follow_unfollow', {'actor_only': False}, name='actstream_follow_all'),
    url(r'^unfollow/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'follow_unfollow', {'do_follow': False}, name='actstream_unfollow'),

    # Follower and Actor lists
    url(r'^followers/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'followers', name='actstream_followers'),
    url(r'^actors/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'actor', name='actstream_actor'),
    url(r'^actors/(?P<content_type_id>\d+)/$',
        'model', name='actstream_model'),
        
    url(r'^new_wall_post/$', view=login_required (views.new_wall_post), name='new_wall_post'),
    url(r'^detail/(?P<action_id>\d+)/$', view=login_required(views.detail), name='actstream_detail'),
    url(r'^(?P<username>[-\w]+)/$', view=login_required (views.user), name='actstream_user'),
    url(r'^$', view=login_required (views.stream), name='actstream'),
    url(r'^new_group_post', view=login_required (views.new_group_post), name='new_group_post'),
)