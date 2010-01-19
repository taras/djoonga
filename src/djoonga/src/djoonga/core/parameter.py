import os.path
import ConfigParser
import StringIO
import os
import re
from djoonga.utils.exceptions import FileDoesNotExist

class JParameter:
    '''
    Helper class for interaction with Joomla Parameter fields.
    http://api.joomla.org/Joomla-Framework/Parameter/JParameter.html
    '''
    def __init__(self, data=None, path=None, namespace='default'):

        self.namespace = namespace

        tmp = StringIO.StringIO()
        tmp.write('[%s]\n'%namespace)

        if not data is None:
            tmp.write(data)
        elif not data is None:
            if not os.path.exists(path):
                raise FileDoesNotExist('%s does not exist.'%path)
            fp = open(path, 'r')
            tmp.write(fp.read())

        tmp.seek(0)

        self.data = ConfigParser.ConfigParser()
        self.data.optionxform = str
        self.data.readfp(tmp)

    def get(self, name, default=None):
        '''
        Get value of a parameter
        '''
        if self.data.has_option(self.namespace, name):
            return self.data.get(self.namespace, name)
        else:
            return default

    def set(self, name, value):
        '''
        Set value of a parameter
        '''
        self.data.set(self.namespace, name, str(value))

    def __str__(self):
        tmp = StringIO.StringIO()
        self.data.write(tmp)
        tmp.seek(0)
        lines = tmp.readlines()
        tmp.close()
        return ''.join([re.sub(' * = *', '=', line, 1) for line in lines[1:]]).strip()
