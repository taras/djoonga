from django.db import models
from djoonga.utils import jconfig
from djoonga.users.models import User
from django.db.models.signals import pre_save, post_init
import logging
import datetime

CONFIRMATION_CHOICES = (
    (0, u'No'),
    (1, u'Yes'),
)

def get_default_attribs():
    return 0

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
    '''
    Joomla Content Article (com_content)
    
    # Create an article
    >>> a1 = Content.objects.create(title='Test Article')
    
    # Create an article with Read More
    >>> a2 = Content.objects.create(introtext='<hr id="system-readmore" />', \
                          title="Read more test item")
    
    '''
    id = models.IntegerField(primary_key=True, editable=False)
    title = models.CharField(max_length=765)
    alias = models.CharField(max_length=765, blank=True)
    title_alias = models.CharField(max_length=765, blank=True)
    introtext = models.TextField()
    fulltext = models.TextField(verbose_name='Body')
    state = models.IntegerField(verbose_name='Published', choices=CONFIRMATION_CHOICES)
    section = models.ForeignKey(Section, db_column='sectionid', blank=True, null=True, default='0')
    mask = models.IntegerField(blank=True, default='0')
    category = models.ForeignKey(Category, db_column='catid', blank=True, null=True, default='0')
    created = models.DateTimeField(blank=True, default=datetime.datetime.now)
    created_by = models.ForeignKey(User, related_name='created', db_column='created_by')
    created_by_alias = models.CharField(max_length=765, blank=True)
    modified = models.DateTimeField(default=datetime.datetime.now)
    modified_by = models.ForeignKey(User, related_name='modified', db_column='modified_by')
    checked_out = models.BooleanField()
    checked_out_time = models.DateTimeField()
    publish_up = models.DateTimeField()
    publish_down = models.DateTimeField()
    images = models.TextField(blank=True)
    urls = models.TextField(blank=True)
    attribs = models.TextField(blank=True, default=get_default_attribs)
    version = models.IntegerField(blank=True, default='1')
    parentid = models.IntegerField(blank=True, default='0')
    ordering = models.IntegerField()
    metakey = models.TextField(blank=True)
    metadesc = models.TextField(blank=True)
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

def post_init_content(sender, **kwargs):
    '''
    Prepares content before using it
    '''
    content = kwargs['instance']
    
    # joining introtext and fulltext
    if content.fulltext:
        content.introtext = '%s<hr id="system-readmore" />%s'%(content.introtext,content.fulltext)

def pre_save_content(sender, **kwargs):
    '''
    Prepares content for saving
    '''
    content = kwargs['instance']
    
    # split introtext and fulltext
    if '<hr id="system-readmore" />' in content.introtext:
        try:
            blank = ''
            content.introtext, blank, content.fulltext = content.introtext.partition('<hr id="system-readmore" />')
        except Exception, e:
            logging.debug('Error occured trying to split body into introtext and fulltext: %s'%str(e))
    
    #Assign 0 to blank Section id
    if hasattr(content, 'section_id') and not content.section_id:
        content.section_id = 0
        
    if hasattr(content, 'category_id') and not content.category_id:
        content.category_id = 0
            
post_init.connect(post_init_content, sender=Content)
pre_save.connect(pre_save_content, sender=Content)