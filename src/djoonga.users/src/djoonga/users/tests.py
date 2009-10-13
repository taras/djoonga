import unittest
from djoonga.users.models import User
from django.contrib.auth.models import User as DjangoUser
from django.test.client import Client
from djoonga.users.middleware import threadlocals

class UsersTestCase(unittest.TestCase):

    def setUp(self):
        c = Client()
        c.login(username='admin', password='admin')

    def testAdminUserExists(self):
        query = User.objects.filter(username='admin')
        self.assert_(len(query) > 0)
        
        admin = query[0]
        self.assert_(admin.id == 62)
        
    def testAdminUserLogin(self):
        
        query = DjangoUser.objects.filter(username='admin')
        self.assert_(len(query) > 0)
        
        admin = query[0]
        self.assert_(admin.username=='admin')
        self.assert_(admin.password=='!')
        self.assert_(admin.is_superuser)
        
    def testLoadingJoomlaAdminUser(self):
        # this test needs to be finished
        # need to implement reference to joomla user