from django.contrib import admin
from models import Content, Section, Category, Rating, FrontpageContent
from django import forms
from django.db import models

class ContentAdminForm(forms.ModelForm):
    
    fulltext = forms.CharField(initial='test', widget=forms.Textarea)
    
    class Meta:
        model = Content

class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access',)
    list_filter = ('section', 'category', 'created_by', 'created')
    search_fields = ['title', 'introtext', 'fulltext']

    form = ContentAdminForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access', 'section', )
    list_filter = ('section',)
    search_fields = ['title', 'description']

class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access',)
    search_fields = ['title', 'description']

admin.site.register(Content, ContentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Section, SectionAdmin)