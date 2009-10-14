from django.contrib import admin
from models import Article, Section, Category, Rating, FrontpageContent
from django import forms
from django.db import models
from django import forms
from djoonga.users.models import JoomlaUser
from django.db.models.query import QuerySet

class ArticleAdminForm(forms.ModelForm):
    introtext = forms.CharField(label="Body",widget=forms.Textarea)
    created_by_alias = forms.CharField(label="Author Alias")
    class Meta:
        model = Article

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'alias' : ['title'] }
    list_display = ('id', 'title', 'ordering', 'access',)
    list_filter = ('section', 'category', 'created_by', 'created')
    search_fields = ['title', 'introtext', 'fulltext']
    exclude = ('fulltext', 'mask', 'modified_by', 'checked_out')
    form = ArticleAdminForm
    
    def get_form(self, request, obj=None, **kwargs):
        # save the currently logged in user for later
        self.current_user = request.user
        return super(ArticleAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, field, **kwargs):
        current_user = self.current_user
        if field.name == 'created_by':
            queryset = JoomlaUser.objects.all()
            return forms.ModelChoiceField(
                queryset=queryset, initial=self.current_user.id)          
        return super(ArticleAdmin, self).formfield_for_dbfield(field, **kwargs)    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access', 'section', )
    list_filter = ('section',)
    search_fields = ['title', 'description']

class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ordering', 'access',)
    search_fields = ['title', 'description']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Section, SectionAdmin)