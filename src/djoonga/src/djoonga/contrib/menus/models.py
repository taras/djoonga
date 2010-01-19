from django.db import models
from djoonga.conf import jconfig

class JMenuItem(models.Model):
    id = models.IntegerField(primary_key=True)
    menu = models.CharField(max_length=225, db_column='menutype')
    name = models.CharField(max_length=765, blank=True)
    alias = models.CharField(max_length=765)
    link = models.TextField(blank=True)
    type = models.CharField(max_length=150)
    published = models.IntegerField()
    parent = models.IntegerField()
    componentid = models.IntegerField()
    sublevel = models.IntegerField(null=True, blank=True)
    ordering = models.IntegerField(null=True, blank=True)
    checked_out = models.IntegerField()
    checked_out_time = models.DateTimeField()
    pollid = models.IntegerField()
    browsernav = models.IntegerField(null=True, db_column='browserNav', blank=True) # Field name made lowercase.
    access = models.IntegerField()
    utaccess = models.IntegerField()
    params = models.TextField()
    lft = models.IntegerField()
    rgt = models.IntegerField()
    home = models.IntegerField()

    class Meta:
        db_table = u'%smenu'%jconfig.dbprefix

    def __str__(self):
        return '(%s) %s'%(self.id, self.name)

class JMenu(models.Model):
    id = models.IntegerField(primary_key=True)
    menutype = models.CharField(unique=True, max_length=225)
    title = models.CharField(max_length=765)
    description = models.CharField(max_length=765)
    class Meta:
        db_table = u'%smenu_types'%jconfig.dbprefix
    def __str__(self):
        return '(%s) %s'%(self.id, self.title)
