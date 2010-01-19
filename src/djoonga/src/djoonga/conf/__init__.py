"""
Settings and configuration from Joomla!.

Values will be read from Joomla! configuration file specified by the
JOOMLA_CONFIGURATION environment variable, and then from
djoonga.conf.global_settings; see the global settings file for
a list of all possible variables.
"""

import os
from djoonga.utils.exceptions import ConfigurationNotFound
import subprocess
import phpserialize
import StringIO

ENVIRONMENT_VARIABLE = "JOOMLA_CONFIGURATION"

try:
    configuration = os.environ[ENVIRONMENT_VARIABLE]
    if not configuration: # If it's set but is an empty string.
        raise KeyError
except KeyError:
    # NOTE: This is arguably an EnvironmentError, but that causes
    # problems with Python's interactive help.
    raise ConfigurationNotFound("Configuration cannot be loaded, because environment variable %s is undefined." % ENVIRONMENT_VARIABLE)

if not os.path.exists(configuration):
    raise ConfigurationNotFound("Configuration file could not be found in %s" % configuration)

path = os.path.abspath(os.path.join(os.getcwd(), configuration))

cmd = ['php','-r','''include('%s'); $config = new JConfig; echo serialize($config);'''%path ]
s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
output, error = s.communicate()
s = StringIO.StringIO()
s.write(output)
s.seek(0)

jconfig = phpserialize.load(s, object_hook=phpserialize.phpobject)

