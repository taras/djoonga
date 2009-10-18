from django.db import models
from django.contrib.auth.models import User
from djoonga.utils import jconfig

USERTYPE_CHOICES = (
    (29, 'Public Frontend'),
    (18, '+- Registered'),
    (19, '+-- Author'),
    (20, '+--- Editor'),
    (21, '+---- Publisher'),
    (31, 'Public Backend'),
    (23, '+- Manager'),
    (24, '+-- Administrator'),
    (25, '+--- Super Administrator'),
)

class JGroup(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = u'%sgroups'%jconfig('dbprefix')
        verbose_name = 'Joomla Group'

    def __unicode__(self):
        return self.name

class JUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    username = models.CharField(max_length=450)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    usertype = models.CharField(max_length=25, editable=False)
    block = models.BooleanField()
    sendemail = models.BooleanField(db_column='sendEmail') # Field name made lowercase.
    gid = models.IntegerField(db_column='gid', default=1, choices=USERTYPE_CHOICES)
    registerdate = models.DateTimeField(db_column='registerDate', blank=True, null=True) # Field name made lowercase.
    lastvisitdate = models.DateTimeField(db_column='lastvisitDate', blank=True, null=True) # Field name made lowercase.
    activation = models.CharField(max_length=300, editable=False)
    params = models.TextField()
    class Meta:
        db_table = u'%susers'%jconfig('dbprefix')
        verbose_name = 'Joomla User'
    
    def __unicode__(self):
        return self.name

class UserReference(models.Model):
    django = models.ForeignKey(User)
    joomla = models.ForeignKey(JUser)

    class Meta:
        db_table = u'djoonga_%suser_reference'%jconfig('dbprefix')
        unique_together = ("django", "joomla")
        verbose_name = 'User Cross Reference'