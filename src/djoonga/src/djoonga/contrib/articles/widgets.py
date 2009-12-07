from django.forms.widgets import Widget, HiddenInput
from django.utils.safestring import mark_safe
from djoonga.categories.models import JSection, JCategory
from django.template import Context, Template
from django.template.loader import get_template

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
        t = get_template('categorytree.html')
        c = Context({"name": name})
        js = t.render(c)
        output = [js]
        output.append(u'<ul id="%s" class="filetree treeview">'%name)
        output.append(u'<li><span class="uncategorized" class="file" rel="-">Uncategorized</span></li>')
        for section in sections:
            output.append(u'<li><span class="folder">%s</span>'%section.title)
            output.append(render_categories(section.id))
            output.append(u'</li>')
        if data == 0:
            data = ''
        output.append('</ul><input type="hidden" name="section" id="id_section" value="%s" id="id_section" />'%data)
        return mark_safe(u'\n'.join(output))

class CategoryTreeHiddenWidget(HiddenInput):
    """
    A widget that handles <input type="hidden"> for fields that have a list
    of values.
    """
    def __init__(self, attrs=None):
        super(CategoryTreeHiddenWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        if value == 0:
            value = ''
        output = ['<input class="hidden_tree" type="hidden" name="category" value="%s" id="id_category" />'%value]
        return mark_safe(u'\n'.join(output))