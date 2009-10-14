from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup

from djoonga.users.models import JoomlaUser, Group

# unregister django models
admin.site.unregister(DjangoUser)
admin.site.unregister(DjangoGroup)

class JoomlaUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'usertype')
    list_filter = ('usertype',)

class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
admin.site.register(JoomlaUser, JoomlaUserAdmin)