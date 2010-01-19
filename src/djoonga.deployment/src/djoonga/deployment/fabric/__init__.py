import os.path
__author__="taras"
__date__ ="$Jan 16, 2010 6:03:01 PM$"

from fabric.api import env
from fabric.state import _AttributeDict
from djoonga.deployment.fabric import db
import getpass
import os

class DjoongaSite(_AttributeDict):
    pass

class JoomlaSite(DjoongaSite):
    '''
    Djonga-Joomla Site Definition
    '''

    def __init__(self, host=None, user=None, configuration=None):
        if host is None:
            host = 'localhost'
        self.host_string = host

        if user is None:
            user = getpass.getuser()
        self.user = user

        if configuration is None:
            configuration = os.path.join(os.getcwd(), 'html', 'configuration.php')
        self.configuration = configuration

    def __call__(self):
        env.host_string = self.host_string
        env.user = self.user
        env.configuration = self.configuration
        db.configure()