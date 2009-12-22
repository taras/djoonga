from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import sys

class Command(BaseCommand):
    help = "Generate a menu chart"
    args = '[optional output]'

    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = False

    def handle(self, output='', *args, **options):

        from django.db.models import Max, Min
        import networkx as nx
        import pygraphviz as pgv
        
        from djoonga.contrib.menus.models import JMenu, JMenuItem    

        g = pgv.AGraph(directed=True)
        g.add_node('Root')
        
        def get_menu_text(type, id):
            return 'Menu: %s (%s)'%(type.encode('ascii', 'ignore'), id)
        
        def get_item_text(name, id):
            return 'Item: %s (%s)'%(name.encode('ascii', 'ignore'), id)
        
        def add_menu(menu, g):
            menu_text = get_menu_text(menu.menutype, menu.id)
            g.add_node(menu_text)
            g.add_edge(menu_text, 'Root')
            print 'Added %s'%menu_text
            
            def add_item(menu, item, g, depth):
                item_text = get_item_text(item.name, item.id)
                
                if depth == 0: # adding top level item
                    menu_text = get_menu_text(menu.menutype, menu.id)
                    g.add_node(item_text)
                    g.add_edge(item_text, menu_text)
                    print 'Added %s to %s.'%(item_text, menu_text)
                else:   # adding sub item
                    prev_item = JMenuItem.objects.get(pk=item.parent)
                    prev_item_text = get_item_text(prev_item.name, prev_item.id)
                    g.add_node(item_text)
                    g.add_edge(item_text, prev_item_text)
                    print 'Added %s to %s.'%(item_text, prev_item_text)
                return g
            
            result = JMenuItem.objects.filter(menu=menu.menutype).aggregate(Min('sublevel'), Max('sublevel'))
            if not result['sublevel__min'] is None and not result['sublevel__max'] is None:
                for depth in range(result['sublevel__min'], result['sublevel__max']):
                    items = JMenuItem.objects.filter(sublevel=depth, menu=menu.menutype)
                    for item in items:
                        g = add_item(menu, item, g, depth)
            
            return g

        menus = JMenu.objects.filter(menutype__contains='mainmenu',)
        for menu in menus:
            g = add_menu(menu, g)
        
        menus = JMenu.objects.filter(menutype__contains='sub',)
        for menu in menus:
            g = add_menu(menu, g)

        menus = JMenu.objects.filter(menutype__contains='related',)
        for menu in menus:
            g = add_menu(menu, g)

        g.write('output.dot')