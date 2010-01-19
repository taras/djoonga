from djoonga.contrib.menus.models import JMenu, JMenuItem
import djoonga.utils.tinytree as tinytree
import cgi

class MenuNode(tinytree.Tree):
    def __init__(self, name, children=None, **kwargs):
        tinytree.Tree.__init__(self, children)
        self.name = name
        self.menu = kwargs.get('menu', False)
        self.ref = kwargs.get('ref', None)
        self.title = kwargs.get('title', '')
        self.values = kwargs

    def __repr__(self):
        
        title = self.values.get('title', 'title missing').encode('ascii', 'ignore')
        if self.ref is None:
            
            return "%s - %s"%(self.name, title)
        else:
            return "%s - %s -> %s"%(self.name, title, self.ref)

def get_menu_tree(menu=None):
    '''
    Get a tree representation of the menu structure.
    '''

    tree = MenuNode('root')

    def add_menu(menu, tree):
        '''
        Add this menu and all of it's items to the tree.
        Return modified tree
        '''
        m = MenuNode(menu.menutype, menu=True, title=menu.title)

        def add_item(m, item):
            '''
            Add current item and all of it's children to the tree.
            Return the modified tree
            '''
            t = MenuNode(item.id, title=item.name, alias=item.alias,
                            link=item.link, type=item.type, published=item.published,
                            params=item.params, menutype=item.menu, ordering=item.ordering)
            qs = cgi.parse_qs(item.link)
            if qs.has_key('index.php?Itemid'):
                t.ref = qs['index.php?Itemid'][0]

            children = JMenuItem.objects.filter(parent=item.id).order_by('ordering')
            if children:
                for child in children:
                    t = add_item(t, child)
            m.addChild(t)
            return m

        items = JMenuItem.objects.filter(menu=menu.menutype, sublevel=0).order_by('ordering')
        if items:
            for item in items:
                m = add_item(m, item)

        tree.addChild(m)
        return tree

    if menu is None:
        menus = JMenu.objects.all()
        for menu in menus:
            result = add_menu(menu, tree)
    else:
        try:
            menu = JMenu.objects.get(menutype=menu)
            result = add_menu(menu, tree)
        except menu.DoesNotExist:
            print "Menu %s does not exist"%menu
            result = None

    return result

def get_urls(menu):
    '''
    Returns list of all urls from a specific menu.
    '''

    def process(node, base):
        '''
        Adds item's url to storage and all of it's children.
        @param node TinyTree node to process
        @param base String url of previous items
        '''

        def add(node, base):
            type = node.values.get('type')
            alias = node.values.get('alias')
            published = node.values.get('published')
            if not (type == 'menulink' or type == 'url') and not published == -2 :
                storage.append('%s/%s'%(base, alias))

        alias = node.values.get('alias')
        add(node, base)
        for child in node.children:
            process(child, '%s/%s'%(base, alias))
    
    tree = get_menu_tree(menu)
    items = tree.children[0].children
    storage = []
    [process(item, '') for item in items]

    return storage

