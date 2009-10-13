from django.contrib import admin
from models import User, Group
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup

# unregister django models
admin.site.unregister(DjangoUser)
admin.site.unregister(DjangoGroup)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'usertype')
    list_filter = ('usertype',)

class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)