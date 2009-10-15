
from south.db import db
from django.db import models
from djoonga.articles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Article.checked_out_time'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column(u'%scontent'%jconfig('dbprefix'), 'checked_out_time', orm['articles.article:checked_out_time'])
        
        # Changing field 'Article.publish_up'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column(u'%scontent'%jconfig('dbprefix'), 'publish_up', orm['articles.article:publish_up'])
        
        # Changing field 'Article.publish_down'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column(u'%scontent'%jconfig('dbprefix'), 'publish_down', orm['articles.article:publish_down'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Article.checked_out_time'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column(u'%scontent'%jconfig('dbprefix'), 'checked_out_time', orm['articles.article:checked_out_time'])
        
        # Changing field 'Article.publish_up'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column(u'%scontent'%jconfig('dbprefix'), 'publish_up', orm['articles.article:publish_up'])
        
        # Changing field 'Article.publish_down'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)))
        db.alter_column(u'%scontent'%jconfig('dbprefix'), 'publish_down', orm['articles.article:publish_down'])
        
    
    
    models = {
        'articles.article': {
            'Meta': {'db_table': "u'%scontent'"%jconfig('dbprefix')},
            'access': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'alias': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'attribs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['articles.Category']", 'null': 'True', 'db_column': "'catid'", 'blank': 'True'}),
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'checked_out_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created'", 'db_column': "'created_by'", 'to': "orm['users.JoomlaUser']"}),
            'created_by_alias': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'fulltext': ('django.db.models.fields.TextField', [], {}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'introtext': ('django.db.models.fields.TextField', [], {}),
            'mask': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'blank': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {'default': "'none'"}),
            'metadesc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'metakey': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'modified'", 'db_column': "'modified_by'", 'default': "'0'", 'to': "orm['users.JoomlaUser']", 'blank': 'True', 'null': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parentid': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'blank': 'True'}),
            'publish_down': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_up': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['articles.Section']", 'null': 'True', 'db_column': "'sectionid'", 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'title_alias': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'urls': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': "'1'", 'blank': 'True'})
        },
        'articles.category': {
            'Meta': {'db_table': "u'%scategories'"%jconfig('dbprefix')},
            'access': ('django.db.models.fields.IntegerField', [], {}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'checked_out': ('django.db.models.fields.IntegerField', [], {}),
            'checked_out_time': ('django.db.models.fields.DateTimeField', [], {}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'image_position': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {}),
            'params': ('django.db.models.fields.TextField', [], {}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'articles.frontpagecontent': {
            'Meta': {'db_table': "u'%scontent_frontpage'"%jconfig('dbprefix')},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']", 'primary_key': 'True', 'db_column': "'content_id'"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        },
        'articles.rating': {
            'Meta': {'db_table': "u'%sarticle_rating'"%jconfig('dbprefix')},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']", 'primary_key': 'True', 'db_column': "'article_id'"}),
            'lastip': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {})
        },
        'articles.section': {
            'Meta': {'db_table': "u'%ssections'"%jconfig('dbprefix')},
            'access': ('django.db.models.fields.IntegerField', [], {}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'checked_out_time': ('django.db.models.fields.DateTimeField', [], {}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.TextField', [], {}),
            'image_position': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {}),
            'params': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'users.joomlauser': {
            'Meta': {'db_table': "u'%susers'"%jconfig('dbprefix')},
            'activation': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'block': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'gid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'lastvisitdate': ('django.db.models.fields.DateTimeField', [], {'db_column': "'lastvisitDate'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'params': ('django.db.models.fields.TextField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'registerdate': ('django.db.models.fields.DateTimeField', [], {'db_column': "'registerDate'"}),
            'sendemail': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'sendEmail'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '450'}),
            'usertype': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        }
    }
    
    complete_apps = ['articles']