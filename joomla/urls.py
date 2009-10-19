
from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns(
    '',
    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

urlpatterns += patterns('',
    (r'^article/', include('djoonga.articles.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
         (r'^media/(?P<path>.+)$', 'media_utils.views.serve_app_media')
    )
