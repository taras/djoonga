from django.db import models
from djoonga.conf import jconfig

class JModule(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    ordering = models.IntegerField(blank=True)
    position = models.CharField(max_length=150, blank=True)
    checked_out = models.IntegerField(blank=True)
    checked_out_time = models.DateTimeField(blank=True)
    published = models.IntegerField(blank=True)
    module = models.CharField(max_length=150, blank=True)
    numnews = models.IntegerField()
    access = models.IntegerField(blank=True)
    showtitle = models.IntegerField(blank=True)
    params = models.TextField(blank=True)
    iscore = models.IntegerField(blank=True)
    client_id = models.IntegerField(blank=True)
    control = models.TextField(blank=True)

    class Meta:
        db_table = u'%smodules'%jconfig.dbprefix

    def __str__(self):
        return '(%s) %s'%(self.id, self.title)

class JModuleMenuRel(models.Model):
    module = models.IntegerField(primary_key=True, db_column='moduleid')
    menu = models.IntegerField(primary_key=True, db_column='menuid')

    class Meta:
        db_table = u'%smodules_menu'%jconfig.dbprefix

    def __str__(self):
        return 'Module %s to Menu %s Relationship'%(self.module, self.menu)