from django.db import models
from djoonga.utils import jconfig

class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    alias = models.CharField(max_length=765)
    image = models.TextField()
    scope = models.CharField(max_length=150)
    image_position = models.CharField(max_length=90)
    description = models.TextField()
    published = models.BooleanField()
    checked_out = models.BooleanField()
    checked_out_time = models.DateTimeField()
    ordering = models.IntegerField()
    access = models.IntegerField()
    count = models.IntegerField()
    params = models.TextField()

    class Meta:
        db_table = u'%ssections'%jconfig('dbprefix')

    def __unicode__(self):
        return self.title

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField()
    title = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    alias = models.CharField(max_length=765)
    image = models.CharField(max_length=765)
    section = models.CharField(max_length=150)
    image_position = models.CharField(max_length=90)
    description = models.TextField()
    published = models.IntegerField()
    checked_out = models.IntegerField()
    checked_out_time = models.DateTimeField()
    editor = models.CharField(max_length=150, blank=True)
    ordering = models.IntegerField()
    access = models.IntegerField()
    count = models.IntegerField()
    params = models.TextField()

    class Meta:
        db_table = u'%scategories'%jconfig('dbprefix')
    
    def __unicode__(self):
        return self.title