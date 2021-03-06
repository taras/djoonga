from django.contrib import admin
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from djoonga.users.models import JUser
from models import JArticle, JSection, JCategory
from widgets import CategoryTreeWidget, CategoryTreeHiddenWidget

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
    section_queryset = JSection.objects.all()
    category_queryset = JCategory.objects.all()
    section = forms.ModelChoiceField(queryset=section_queryset, label='Section/Category', widget=CategoryTreeWidget, required=False)
    category = forms.ModelChoiceField(queryset=category_queryset, label=None, widget=CategoryTreeHiddenWidget, required=False)
    class Meta:
        model = JArticle
        exclude = ('fulltext', 'mask', 'modified_by', 'checked_out',)
        
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'alias' : ['title'] }
    list_display = ('title', 'state', 'ordering', 'access', 'section_', 'category_', 'created_by', 'date', 'hits', 'id')
    list_filter = ('section', 'category', 'created_by', 'created')
    search_fields = ['title', 'introtext', 'fulltext']
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
        if field.name == 'section':
            print kwargs
        if field.name == 'created_by':
            # save current user into created_by when item created through admin
            queryset = JUser.objects.all()
            return forms.ModelChoiceField(
                queryset=queryset, initial=self.current_user.id)          
        return super(ArticleAdmin, self).formfield_for_dbfield(field, **kwargs)

admin.site.register(JArticle, ArticleAdmin)