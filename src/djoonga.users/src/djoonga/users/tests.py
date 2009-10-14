import unittest
from djoonga.users.models import JoomlaUser
from djoonga.users.models import UserReference
from django.contrib.auth.models import User as DjangoUser
from django.test.client import Client

class UsersTestCase(unittest.TestCase):

    def setUp(self):
        c = Client()
        c.login(username='admin', password='admin')

    def testJoomlaAdminUserExists(self):
        admin = JoomlaUser.objects.get(username='admin')
        self.assert_(admin != None)
        self.assert_(admin.id == 62)
        
    def testAdminUserLogin(self):
        admin = DjangoUser.objects.get(username='admin')
        self.assert_(admin != None)
        self.assert_(admin.username=='admin')
        self.assert_(admin.password=='!')
        self.assert_(admin.is_superuser)
        self.assert_(admin.is_active)
        
    def testUserCrossReference(self):
        joomla_user = JoomlaUser.objects.get(username='admin')
        django_user = DjangoUser.objects.get(username='admin')
        
        reference = UserReference.objects.get(joomla=joomla_user, django=django_user)
        self.assert_(isinstance(reference, UserReference))
        
        self.assert_(UserReference.objects.get(joomla=joomla_user).django == django_user)
        self.assert_(UserReference.objects.get(django=django_user).joomla == joomla_user)        