from django.db import models
from django.contrib.auth.models import User as DjangoUser
from djoonga.utils import jconfig

class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    class Meta:
        db_table = u'%sgroups'%jconfig('dbprefix')

    def __unicode__(self):
        return self.name

class JoomlaUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    username = models.CharField(max_length=450)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    usertype = models.CharField(max_length=75)
    block = models.IntegerField()
    sendemail = models.IntegerField(null=True, db_column='sendEmail', blank=True) # Field name made lowercase.
    gid = models.IntegerField()
    registerdate = models.DateTimeField(db_column='registerDate') # Field name made lowercase.
    lastvisitdate = models.DateTimeField(db_column='lastvisitDate') # Field name made lowercase.
    activation = models.CharField(max_length=300)
    params = models.TextField()
    class Meta:
        db_table = u'%susers'%jconfig('dbprefix')
    
    def __unicode__(self):
        return self.name

class UserReference(models.Model):
    django = models.ForeignKey(DjangoUser)
    joomla = models.ForeignKey(JoomlaUser)

    class Meta:
        db_table = u'djoonga_%suser_reference'%jconfig('dbprefix')
        unique_together = ("django", "joomla")