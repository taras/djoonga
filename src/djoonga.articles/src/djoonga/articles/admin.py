from django.contrib import admin
from models import Article, Section, Category, Rating, FrontpageContent
from django import forms
from django.db import models
from django import forms
from djoonga.users.models import JoomlaUser
from django.db.models.query import QuerySet
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def make_published(modelAdmin, request, queryset):
    queryset.update(state=1)
make_published.short_description = "Publish selected items"

def make_archived(modelAdmin, request, queryset):
    queryset.update(state=-1)
make_archived.short_description = "Archive selected items"

def make_unarchived(modelAdmin, request, queryset):
    queryset.update(state=0)
make_unarchived.short_description = "Unarchive selected items"

def move_items(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect(reverse('djoonga.articles.views.move', args=(ct.pk,)))
move_items.short_description = "Move selected items"

class ArticleAdminForm(forms.ModelForm):
    introtext = forms.CharField(label="Body",widget=forms.Textarea)
    created_by_alias = forms.CharField(label="Author Alias")
    class Meta:
        model = Article

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'alias' : ['title'] }
    list_display = ('title', 'state', 'ordering', 'access', 'section_', 'category_', 'created_by', 'date', 'hits', 'id')
    list_filter = ('section', 'category', 'created_by', 'created')
    search_fields = ['title', 'introtext', 'fulltext']
    exclude = ('fulltext', 'mask', 'modified_by', 'checked_out')
    form = ArticleAdminForm
    actions = [make_published, make_archived, make_unarchived, move_items]
    
    def section_(self, object):
        return object.section.title
    
    def category_(self, object):
        return object.category.title
    
    def date(self, object):
        return object.created

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