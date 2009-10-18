
from south.db import db
from django.db import models
from djoonga.users.models import *
from djoonga.utils import jconfig

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'JUser.lastvisitdate'
        # (to signature: django.db.models.fields.DateTimeField(null=True, db_column='lastvisitDate', blank=True))
        db.alter_column(u'jos_users', 'lastvisitdate', orm['users.juser:lastvisitdate'])
        
        # Changing field 'JUser.registerdate'
        # (to signature: django.db.models.fields.DateTimeField(null=True, db_column='registerDate', blank=True))
        db.alter_column(u'jos_users', 'registerdate', orm['users.juser:registerdate'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'JUser.lastvisitdate'
        # (to signature: django.db.models.fields.DateTimeField(db_column='lastvisitDate'))
        db.alter_column(u'jos_users', 'lastvisitdate', orm['users.juser:lastvisitdate'])
        
        # Changing field 'JUser.registerdate'
        # (to signature: django.db.models.fields.DateTimeField(db_column='registerDate'))
        db.alter_column(u'jos_users', 'registerdate', orm['users.juser:registerdate'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.jgroup': {
            'Meta': {'db_table': "u'%sgroups'"%jconfig('dbprefix')},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'users.juser': {
            'Meta': {'db_table': "u'%susers'"%jconfig('dbprefix')},
            'activation': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'block': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_column': "'gid'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'lastvisitdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'lastvisitDate'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'params': ('django.db.models.fields.TextField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'registerdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'registerDate'", 'blank': 'True'}),
            'sendemail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'sendEmail'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '450'}),
            'usertype': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'users.userreference': {
            'Meta': {'unique_together': "(('django', 'joomla'),)", 'db_table': "u'djoonga_jos_user_reference'"},
            'django': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joomla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.JUser']"})
        }
    }
    
    complete_apps = ['users']
