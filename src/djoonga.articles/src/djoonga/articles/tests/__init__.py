import unittest
import os
import inspect
from djoonga.articles.models import Article
from django.test.client import Client
from djoonga.users.models import JoomlaUser
from django.core import management

class ArticlesTestCase(unittest.TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        tests = os.path.dirname(inspect.currentframe().f_code.co_filename)
        management.call_command('loaddata', os.path.join(tests, 'fixtures/users.json'), verbosity=0)
        
        c = Client()
        c.login(username='admin', password='admin')
        
    def testCreateArticleModel(self):
        '''
        Creating articles
        '''
        user = JoomlaUser.objects.get(username='admin')
        article = Article.objects.create(title='Test article', introtext='some text', created_by=user)
        
        