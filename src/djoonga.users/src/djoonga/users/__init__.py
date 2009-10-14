import subprocess, os, logging

from djoonga.users.models import JoomlaUser
from djoonga.users.models import UserReference
from django.contrib.auth.models import User as DjangoUser
from django.conf import settings

class JoomlaAuthenticationBackend:
    def authenticate(self, username=None, password=None):
        try:
            joomla_user = JoomlaUser.objects.get(username=username)
        except JoomlaUser.DoesNotExist:
            return None
        
        # check if user is blocked
        if joomla_user.block:
            return None
        
        crypt, salt = joomla_user.password.split(':')
        helper = os.path.join(settings.JOOMLA_SITEPATH, 'libraries', 'joomla', 'user','helper.php')
        cmd = ['php', '-r', "include('%s'); echo JUserHelper::getCryptedPassword('%s','%s');"%(helper, password, salt)]
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        testcrypt, error = s.communicate()
        if error:
            logging.debug(error)

        # check if the entered password matches joomla user's password
        if crypt != testcrypt:
            return None
        
        try:
            django_user = DjangoUser.objects.get(username__exact=username)
        except DjangoUser.DoesNotExist:
            django_user = DjangoUser.objects.create_user(username, joomla_user.email, '')
            django_user.set_unusable_password()
            django_user.is_superuser = joomla_user.usertype == 'Super Administrator'
            django_user.is_staff = joomla_user.usertype == 'Super Administrator'
            django_user.is_active = not joomla_user.block
            django_user.save()
            
            reference = UserReference(django=django_user, joomla=joomla_user)
            reference.save()
            
        return django_user
    
    def get_user(self, user_id):
        try:
            return DjangoUser.objects.get(pk=user_id)
        except DjangoUser.DoesNotExist:
            return None