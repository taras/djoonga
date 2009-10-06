from django.contrib import admin
from models import User, Group

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'usertype')
    list_filter = ('usertype',)

class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)