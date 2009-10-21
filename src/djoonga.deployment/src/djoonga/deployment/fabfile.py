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

def restore():
    '''
    Restore mysql database from sql dump file.
    '''
    def listfiles(path):
        a = [s for s in os.listdir(path)
             if os.path.isfile(os.path.join(path, s))]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(path, s)))
        return a
    selected = None
    backups = listfiles('db/backups')
    if len(backups) > 1:
        backups.insert(0, 'last')
    while selected is None:
        print 'Available backups (sorted by creation date):'
        position = 0
        for file in backups:
            position += 1
            name, ext = os.path.splitext(file)
            print ' %s %s' % (position, name)
        selected = prompt('Enter backup number to import: ')
        if not selected.isdigit():
            print 'Please enter a number between 1 and %s\n' % len(backups)
            selected = None
        elif int(selected) < 0 or int(selected) > len(backups):
            print 'Please enter a number between 1 and %s\n' % len(backups)
            selected = None
    selected = int(selected)
    if selected == 1:
        path = 'db/last'
    else:
        path = os.path.join('db', 'backups', backups[selected-1])
    mysqlimport(path)

def mysqlimport(src):
    '''
    Run mysql import command
    '''
    require('dbhost')
    require('dbname')
    require('dbuser')
    require('dbpassword')    
    local('mysql --default_character_set=utf8 --host=%s --user=%s --pass="%s" %s < %s'%\
        (env.dbhost, env.dbuser, env.dbpassword, env.dbname, src))

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
