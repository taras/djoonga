from django.contrib import admin
from djoonga.categories.models import JSection, JCategory

class JCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access', 'section', )
    list_filter = ('section',)
    search_fields = ['title', 'description']

class JSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access',)
    search_fields = ['title', 'description']
    
admin.site.register(JCategory, JCategoryAdmin)
admin.site.register(JSection, JSectionAdmin)