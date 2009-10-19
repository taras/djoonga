from django.contrib import admin
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.widgets import Widget
from django.forms.util import flatatt
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils import simplejson as json
from djoonga.users.models import JUser
from models import JArticle, JRating, JFrontpage
from djoonga.categories.models import JSection, JCategory

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

class CategoryTreeWidget(Widget):

    class Media:
        css = { 'screen': ('articles/jquery.treeview.css',) }
        js = ('articles/jquery.js', 'articles/jquery.treeview.js')
    
    def __init__(self, attrs=None):
        super(CategoryTreeWidget, self).__init__(attrs)
    
    def render(self, name, data, attrs=None):
        def render_categories(section_id):
            categories = JCategory.objects.filter(section=section_id)
            if categories:
                output = [u'<ul>']
                for category in categories:
                    output.append(u'<li><span class="file" rel="%s-%s">%s</span></li>' % (
                        section_id, category.id, category.title))
                output.append(u'</ul>')
                return u'\n'.join(output)
            return u''
                
        sections = JSection.objects.all()
        output = ['''
        <style type="text/css">
            #browser {
              font-family: Verdana, helvetica, arial, sans-serif;
              font-size: 68.75%;
            }
            #browser ul li{
                list-style-type: none;
                cursor: pointer;
            }
            #browser li{
                list-style-type: none;
            }
            #browser ul {
                margin-left: 0px;
                padding-left: 0px;
            }
            </style>
        <script>
            $(document).ready(function(){
                $("#browser").treeview({
                    animated: "fast"
                });
              
            $("#browser li li span").click(function () {
                rel = $(this).attr('rel');
                ids = rel.split('-');
                $('#id_section').attr('value', ids[0]);
                $('#id_category').attr('value', ids[1]);
            });
            
            });
        </script>
        ''']
        output.append(u'<ul id="browser" class="filetree treeview">')
        for section in sections:
            output.append(u'<li><span class="folder">%s</span>'%section.title)
            output.append(render_categories(section.id))
            output.append(u'</li>')
        output.append('</ul><input type="hidden" name="id_section" value="" id="id_section" /><input type="hidden" name="id_category" value="" id="id_category" />')
        return mark_safe(u'\n'.join(output))
        
class ArticleAdminForm(forms.ModelForm):
    introtext = forms.CharField(label="Body",widget=forms.Textarea)
    created_by_alias = forms.CharField(label="Author Alias")
    section = forms.CharField(label='Section/Category', widget=CategoryTreeWidget)
    class Meta:
        model = JArticle

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
            queryset = JUser.objects.all()
            return forms.ModelChoiceField(
                queryset=queryset, initial=self.current_user.id)          
        return super(ArticleAdmin, self).formfield_for_dbfield(field, **kwargs)

admin.site.register(JArticle, ArticleAdmin)