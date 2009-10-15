from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<ct>\d{2})/$', 'djoonga.articles.views.move'),
)
