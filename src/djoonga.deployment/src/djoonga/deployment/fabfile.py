import os
import hashlib
from fabric.api import run, get, local, prompt, require, env, hosts
from tempfile import mkdtemp
from datetime import datetime
from djoonga.utils import jconfig

def mysqldump():
    '''
    Run mysqldump and return the result
    '''
    require('dbhost')
    require('dbname')
    require('dbuser')
    require('dbpassword')
    
    return run('mysqldump --host=%s --user=%s --password=%s %s --quick --lock-tables --add-drop-table'%(env.dbhost, env.dbuser, env.dbpassword, env.dbname))

def backup():
    '''
    Backups mysql database on remote server.
    Downloads the backup and places it in db/backups directory
    Sets db/last symbolic link to point to backup file.
    '''

    backup_name = ''
    while not backup_name:
        backup_name = prompt('What should I name this backup?')
        backup_name = backup_name.lower().replace(' ', '_')
        backup_file_name = 'db/backups/%s.sql'%backup_name
        if not backup_name:
            print 'Backup name must not be empty.'
        elif os.path.exists(backup_file_name):
            backup_name = ''
            print 'Backup file name %s.sql already exists.'%backup_file_name
            print 'Please, enter another backup name.'
    
    output = mysqldump()
    if output:
        fp = open(backup_file_name, 'w')
        fp.write(output)
        fp.close()
    
    local('ln -f %s db/last'%backup_file_name)

def _set_db_settings():
    '''
    Load db settings
    '''
    require('configuration')
    config = jconfig(path=_download_to_tmp(env.configuration))
    env.dbname = config.db
    env.dbuser = config.user
    env.dbpassword = config.password
    env.dbhost = config.host

def _download_to_tmp(src):
    '''
    Downloads contents of file to tmp file. File exists until it's deleted.
    '''
    tmp = mkdtemp()
    name = hashlib.md5(str(datetime.now())).hexdigest()
    dest = os.path.join(tmp, name)
    get(src, dest)
    return dest
