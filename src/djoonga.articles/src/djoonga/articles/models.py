from django.db import models
from djoonga.utils import jconfig
from djoonga.users.models import JoomlaUser
from django.contrib.auth.models import User as DjangoUser
from django.db.models.signals import pre_save, post_init
import logging
from datetime import timedelta, datetime

CONFIRMATION_CHOICES = (
    (0, u'No'),
    (1, u'Yes'),
    (-1, u'Archived'),
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

class Article(models.Model):
    title = models.CharField(max_length=765)
    alias = models.SlugField(blank=True)
    title_alias = models.CharField(max_length=765, blank=True)
    introtext = models.TextField()
    fulltext = models.TextField()
    state = models.IntegerField(verbose_name='Published', choices=CONFIRMATION_CHOICES, default=1)
    section = models.ForeignKey(Section, db_column='sectionid', blank=True, null=True, default='0')
    mask = models.IntegerField(blank=True, default='0')
    category = models.ForeignKey(Category, db_column='catid', blank=True, null=True, default='0')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(JoomlaUser, verbose_name='Author', related_name='created', db_column='created_by')
    created_by_alias = models.CharField(max_length=765, blank=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(JoomlaUser, related_name='modified', db_column='modified_by', blank=True, null=True, default='0')
    checked_out = models.BooleanField()
    checked_out_time = models.DateTimeField(blank=True, null=True)
    publish_up = models.DateTimeField(blank=True, null=True)
    publish_down = models.DateTimeField(blank=True, null=True)
    images = models.TextField(blank=True)
    urls = models.TextField(blank=True)
    attribs = models.TextField(blank=True)
    version = models.IntegerField(blank=True, default='1')
    parentid = models.IntegerField(blank=True, default='0')
    ordering = models.IntegerField(default=0)
    metakey = models.TextField(blank=True)
    metadesc = models.TextField(blank=True)
    access = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    metadata = models.TextField(default='none')
    class Meta:
        db_table = u'%scontent'%jconfig('dbprefix')

    def __unicode__(self):
        return self.title
    
class FrontpageContent(models.Model):
    article = models.ForeignKey(Article, db_column='content_id', primary_key=True)
    ordering = models.IntegerField()
    class Meta:
        db_table = u'%scontent_frontpage'%jconfig('dbprefix')

class Rating(models.Model):
    article = models.ForeignKey(Article, db_column='article_id', primary_key=True)
    rating_sum = models.IntegerField()
    rating_count = models.IntegerField()
    lastip = models.CharField(max_length=150)
    class Meta:
        db_table = u'%sarticle_rating'%jconfig('dbprefix')

def post_init_article(sender, **kwargs):
    '''
    Prepares article before using it
    '''
    article = kwargs['instance']
    
    # joining introtext and fulltext
    if article.fulltext:
        article.introtext = '%s<hr id="system-readmore" />%s'%(article.introtext,article.fulltext)


def pre_save_article(sender, **kwargs):
    '''
    Prepares article for saving
    '''
    article = kwargs['instance']
    
    # split introtext and fulltext
    if '<hr id="system-readmore" />' in article.introtext:
        try:
            blank = ''
            article.introtext, blank, article.fulltext = article.introtext.partition('<hr id="system-readmore" />')
        except Exception, e:
            logging.debug('Error occured trying to split body into introtext and fulltext: %s'%str(e))
    
    #Assign 0 to blank Section id
    if hasattr(article, 'section_id') and not article.section_id:
        article.section_id = 0
        
    if hasattr(article, 'category_id') and not article.category_id:
        article.category_id = 0

    if hasattr(article, 'modified_by_id') and not article.modified_by_id:
        article.modified_by_id = 0
    
post_init.connect(post_init_article, sender=Article)
pre_save.connect(pre_save_article, sender=Article)