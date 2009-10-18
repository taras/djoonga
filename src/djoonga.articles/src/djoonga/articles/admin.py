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
from django.forms import widgets, Field
from django.forms.widgets import Select
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.html import escape, conditional_escape

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

class CategorySelect(Select):
    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label, attrs):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            attrs_html = []
            for k, v in attrs.items():
                attrs_html.append('%s="%s"' % (k, escape(v)))
            if attrs_html:
                attrs_html = " " + " ".join(attrs_html)
            else:
                attrs_html = ""
            return u'<option value="%s"%s%s>%s</option>' % (
                escape(option_value), selected_html, attrs_html,
                conditional_escape(force_unicode(option_label)))
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label, option_attrs in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label,
                    option_attrs))
        return u'\n'.join(output)

class ArticleAdminForm(forms.ModelForm):
    introtext = forms.CharField(label="Body",widget=forms.Textarea)
    created_by_alias = forms.CharField(label="Author Alias")
    section = CategorySelect(choices=(
        (1, "option 1", {"label": "label 1"}),
        (2, "option 2", {"label": "label 2"}),
    ))
    
    #section = forms.ChoiceField(widget = forms.Select(), 
    #               choices = ([('1','1'), ('2','2'),('3','3'), ]), initial='3', required = True,)
    
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