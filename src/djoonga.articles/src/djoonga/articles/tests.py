import unittest
from djoonga.articles.models import Article
from django.test.client import Client

class ArticlesTestCase(unittest.TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        c = Client()
        c.login(username='admin', password='admin')
        
    def testCreateArticleModel(self):
        '''
        Creating articles
        '''
        
        article = Article.objects.create(title='Test article', introtext='some text')
        
        