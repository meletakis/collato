import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from applications import settings

try:
    from django.utils import timezone
    now = timezone.now
except ImportError:
    now = datetime.datetime.now




def action_handler(verb, **kwargs):
    """
    Handler function to create Action instance upon action signal call.
    """
    from applications.models import Action

    kwargs.pop('signal', None)
    actor = kwargs.pop('sender')
    check_actionable_model(actor)

    # We must store the unstranslated string
    # If verb is an ugettext_lazyed string, fetch the original string
    if hasattr(verb, '_proxy____args'):
        verb = verb._proxy____args[0]

    newaction = Action(
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        verb=unicode(verb),
        public=bool(kwargs.pop('public', True)),
        description=kwargs.pop('description', None),
        timestamp=kwargs.pop('timestamp', now())
    )

    for opt in ('target', 'action_object'):
        obj = kwargs.pop(opt, None)
        if not obj is None:
            check_actionable_model(obj)
            setattr(newaction, '%s_object_id' % opt, obj.pk)
            setattr(newaction, '%s_content_type' % opt,
                    ContentType.objects.get_for_model(obj))
    if settings.USE_JSONFIELD and len(kwargs):
        newaction.data = kwargs
    newaction.save()
