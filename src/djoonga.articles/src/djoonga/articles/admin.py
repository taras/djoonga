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
from django.forms import widgets
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.html import escape, conditional_escape
from django.forms.widgets import Widget
from django.forms.util import flatatt
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
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

class CategorySelect(Widget):
    def __init__(self, attrs=None, choices=()):
        super(CategorySelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            if option_value:
                option_section = Section.objects.filter(id=Category.objects.filter(id=option_value).values('section')).values_list('title')
                if len(option_section):
                    option_section = option_section[0]
                    if len(option_section):
                        option_section = option_section[0]
            else:
                option_section = None
            return u'<option tag="%s" value="%s"%s>%s</option>' % (
                option_section, escape(option_value), selected_html,
                conditional_escape(force_unicode(option_label)))
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label))
        return u'\n'.join(output)
        
class ArticleAdminForm(forms.ModelForm):
    introtext = forms.CharField(label="Body",widget=forms.Textarea)
    created_by_alias = forms.CharField(label="Author Alias")
    section = forms.ModelChoiceField(Section.objects, empty_label='Uncategorized')
    category = forms.ModelChoiceField(Category.objects, empty_label='Uncategorized', widget=CategorySelect)
    
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