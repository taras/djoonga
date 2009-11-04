from djoonga.conf.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

JOOMLA_SITEPATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')), 'html')

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'south',
    'media_utils'
)