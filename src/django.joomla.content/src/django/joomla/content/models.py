from django.db import models
from django.joomla.utils import jconfig
from django.joomla.users.models import User
from django.db.models.signals import pre_save, post_init

CONFIRMATION_CHOICES = (
    (0, u'No'),
    (1, u'Yes'),
)

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

class Content(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765)
    alias = models.CharField(max_length=765)
    title_alias = models.CharField(max_length=765)
    introtext = models.TextField()
    fulltext = models.TextField(verbose_name='Body')
    state = models.IntegerField(verbose_name='Published', choices=CONFIRMATION_CHOICES)
    section = models.ForeignKey(Section, db_column='sectionid')
    mask = models.IntegerField()
    category = models.ForeignKey(Category, db_column='catid')
    created = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name='created', db_column='created_by')
    created_by_alias = models.CharField(max_length=765)
    modified = models.DateTimeField()
    modified_by = models.ForeignKey(User, related_name='modified', db_column='modified_by')
    checked_out = models.BooleanField()
    checked_out_time = models.DateTimeField()
    publish_up = models.DateTimeField()
    publish_down = models.DateTimeField()
    images = models.TextField()
    urls = models.TextField()
    attribs = models.TextField()
    version = models.IntegerField()
    parentid = models.IntegerField()
    ordering = models.IntegerField()
    metakey = models.TextField()
    metadesc = models.TextField()
    access = models.IntegerField()
    hits = models.IntegerField()
    metadata = models.TextField()
    class Meta:
        db_table = u'%scontent'%jconfig('dbprefix')

    def __unicode__(self):
        return self.title

class FrontpageContent(models.Model):
    content = models.ForeignKey(Content, db_column='content_id', primary_key=True)
    ordering = models.IntegerField()
    class Meta:
        db_table = u'%scontent_frontpage'%jconfig('dbprefix')

class Rating(models.Model):
    content = models.ForeignKey(Content, db_column='content_id', primary_key=True)
    rating_sum = models.IntegerField()
    rating_count = models.IntegerField()
    lastip = models.CharField(max_length=150)
    class Meta:
        db_table = u'%scontent_rating'%jconfig('dbprefix')

def prep_content(sender, **kwargs):
    '''
    Prepare content before using it
    '''
    content = kwargs['instance']
    print content.introtext
    print content.fulltext

post_init.connect(prep_content, sender=Content)