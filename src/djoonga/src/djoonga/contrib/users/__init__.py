import os
import subprocess
from django.contrib.auth.models import User
from django.conf import settings

from models import JUser
from models import UserReference

class JoomlaAuthenticationBackend:
    def authenticate(self, username=None, password=None):
        try:
            joomla_user = JUser.objects.get(username=username)
        except JUser.DoesNotExist:
            return None
        
        is_active = not joomla_user.block
        is_staff = joomla_user.gid >= 19
        is_superuser = joomla_user.gid == 25
        
        if not ( is_active and is_staff ):
            return None
        
        crypt, salt = joomla_user.password.split(':')
        helper = os.path.join(settings.JOOMLA_SITEPATH, 'libraries', 'joomla', 'user','helper.php')
        cmd = ['php', '-r', "include('%s'); echo JUserHelper::getCryptedPassword('%s','%s');"%(helper, password, salt)]
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        testcrypt, error = s.communicate()

        # check if the entered password matches joomla user's password
        if crypt != testcrypt:
            return None
        
        try:
            django_user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            django_user = User.objects.create_user(username, joomla_user.email, '')
            django_user.set_unusable_password()
            django_user.is_superuser = is_superuser
            django_user.is_staff = is_staff
            django_user.is_active = is_active
            django_user.save()
            
            reference = UserReference(django=django_user, joomla=joomla_user)
            reference.save()
            
        return django_user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None