from djoonga.users.models import User
import logging

# threadlocals middleware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
def get_current_user():
    django_user = getattr(_thread_locals, 'user', None)
    try:
        joomla_user = User.objects.filter(username=django_user.username)[0]
    except IndexError:
        logging.debug('Could not find joomla user for logged in user')
        joomla_user = None
    return joomla_user

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
