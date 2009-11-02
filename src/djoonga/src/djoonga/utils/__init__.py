import os
import subprocess
import phpserialize
from exceptions import ConfigurationNotFound
import StringIO

class JConfigSerializer(object):
    
    def __init__(self, path=None):

        if path:
            if not os.path.exists(path):
                raise ConfigurationNotFound            
            
            cmd = ['php','-r','''include('%s'); $config = new JConfig; echo serialize($config);'''%path ]
            s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output, error = s.communicate()
            s = StringIO.StringIO()
            s.write(output)
            s.seek(0)
            self.fp = s
    
    def load(self, fp=None):
        if fp:
            return phpserialize.load(fp, object_hook=phpserialize.phpobject)
        else:
            return phpserialize.load(self.fp, object_hook=phpserialize.phpobject)

def jconfig(name=None, path='html/configuration.php'):
    '''
    Get Value from jconfig
    
    name string configuration value to return
    path string path to configuration file
    
    '''
    
    jconfig = JConfigSerializer(path).load()
    if name:
        return getattr(jconfig, name, None)
    
    return jconfig