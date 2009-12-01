from django.contrib import admin
from django.contrib.auth.models import User as User
from django.contrib.auth.models import Group as Group
from django.contrib.auth.models import Permission as Permission

from djoonga.users.models import JUser, JGroup

# unregister django models
#admin.site.unregister(DjangoUser)
#admin.site.unregister(DjangoGroup)

class JUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'usertype')
    list_filter = ('usertype',)

admin.site.register(JUser, JUserAdmin)
