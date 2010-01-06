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

def get_menu_tree():

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
                            params=item.params, menutype=item.menu)
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

    menus = JMenu.objects.all()
    for menu in menus:
        tree = add_menu(menu, tree)

    return tree