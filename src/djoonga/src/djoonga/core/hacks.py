__author__="taras"
__date__ ="$Jan 13, 2010 12:06:32 PM$"

from django.db import connection
from django.template import Context, Template

def fix_datetime(table, fields, **kwargs):
    '''
    This decorator can be used on functions that cause CREATE or UPDATE to be
    performed in tables with datetime field that has default 0000-00-00 00:00:00
    Django 1.0.1 does not support datetime default value of 0000-00-00 00:00:00
    so we resort to this fix.

    @param str table String name of table to update
    @param variable fields String or Tuple of Strings of field names

        Usage:
        
    from djoonga.core.hacks import fix_datetime
    @fix_datetime('%smodule'%jconfig('prefix'), 'checked_out_time')
    def save(item):
        item.save()

        or

    from djoonga.core.hacks import fix_datetime
    @fix_datetime('%scontent'%jconfig('prefix'), ('created', 'modified))
    def save(item):
        item.save()

    PS: I know this sucks, because it adds 3 queries to every CREATE and UPDATE query.
    If you have a better solution, please let me know. I'm hoping that Django
    will have a solution to 0000-00-00 00:00:00 MySQL datetime issue or Joomla
    will start using NULL instead of 0000-00-00 00:00:00.
    '''
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            if not table:
                raise Exception('table field can not be empty')
            if not fields:
                raise Exception('Specify atleast one field in fields as string or tuple of strings')
            if isinstance(fields, str):
                before = Template('''
                    ALTER TABLE `{{ table }}` CHANGE `{{ fields }}` `{{ fields }}` datetime NULL DEFAULT '0000-00-00 00:00:00';
                ''')
                after = Template('''
                    UPDATE `{{ table }}` SET `{{ fields }}`='0000-00-00 00:00:00' WHERE `{{ fields }}` IS NULL;
                    ALTER TABLE `{{ table }}` CHANGE `{{ fields }}` `{{ fields }}` datetime NOT NULL DEFAULT '0000-00-00 00:00:00';
                ''')
            elif isinstance(fields, tuple):
                before = Template('''
                    ALTER TABLE `{{ table }}`
                    {% for field in fields %}
                        CHANGE `{{ field }}` `{{ field }}` datetime NULL DEFAULT '0000-00-00 00:00:00'
                        {% if not forloop.last %},{% endif %}
                    {% endfor %};
                ''')
                after = Template('''
                    {% for field in fields %}UPDATE `{{ table }}` SET `{{ field }}`='0000-00-00 00:00:00' WHERE `{{ field }}` IS NULL;{% endfor %}
                    ALTER TABLE `{{ table }}` {% for field in fields %} CHANGE `{{ field }}` `{{ field }}` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'{% if not forloop.last %},{% endif %}{% endfor %};
                ''')
            c = Context({"table":table, "fields":fields})
            before_query = before.render(c)
            after_query = after.render(c)
            cursor = connection.cursor()
            cursor.execute(before_query)
            cursor.fetchone()
            result = f(*args, **kwargs)
            cursor.execute(after_query)
            cursor.fetchone()
            return result
        wrapped_f.__doc__ = f.__doc__
        wrapped_f.__name__ = f.__name__
        wrapped_f.__module__ = f.__module__
        return wrapped_f
    return wrap

