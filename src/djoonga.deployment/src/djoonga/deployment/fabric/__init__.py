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

    def __init__(self, host='localhost', user=getpass.getuser(), configuration=os.path.join(os.getcwd(), 'html', 'configuration.php'), base='~'):
        self.user = user
        self.configuration = configuration
        self.host_string = host
        self.base = base

    def __call__(self):
        env.host_string = self.host_string
        env.user = self.user
        env.configuration = self.configuration
        env.base = self.base
        db.configure()