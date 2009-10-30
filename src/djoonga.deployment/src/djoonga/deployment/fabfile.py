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
    
    return run('mysqldump --host=%s --user=%s --password=%s %s --quick \
               --lock-tables --add-drop-table'% \
               (env.dbhost, env.dbuser, env.dbpassword, env.dbname))

def _prompt_for_backup_name(base_path='db'):
    '''
    Prompts for new backup name. Verifies that existing file with same name does
    not exist. Returns ( backup_name, backup_path ) 
    '''
    backup_name = ''
    while not backup_name:
        backup_name = prompt('What should I name this backup?')
        backup_name = backup_name.lower().replace(' ', '_')
        backup_path = os.path.join('db', '%s.sql'%backup_name)
        if not backup_name:
            print 'Backup name must not be empty.'
        elif os.path.exists(backup_path):
            backup_name = ''
            print 'Backup file name %s.sql already exists.'%backup_file_name
            print 'Please, enter another backup name.'
    return backup_name, backup_path    

def backup():
    '''
    Backups mysql database on remote server.
    Downloads the backup and places it in db/backups directory
    Sets db/last symbolic link to point to backup file.
    '''
    
    backup_name, backup_path = _prompt_for_backup_name()
    env.backup = (backup_name, backup_path)
    
    output = mysqldump()
    if output:
        fp = open(backup_path, 'w')
        fp.write(output)
        fp.close()
    
    local('ln -f %s db/last'%backup_path)

def _select_backup(src='db'):
    '''
    Select from available list of backups.
    '''
    def listfiles(path):
        a = [s for s in os.listdir(path)
             if os.path.isfile(os.path.join(path, s))]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(path, s)))
        return a

    if not os.path.exists(src):
        print '%s directory does not exist'
        return None, None
    
    selected = None
    backups = listfiles(src)

    # return nothing if there are no backup files
    if len(backups) == 0:
        print 'There are no backups available'
        return None, None

    if 'last' in backups:
        f = open(os.path.join(src, 'last'), 'r')
        last = _md5sum(f)
        f.close()
    else:
        last = None

    while selected is None:
        print 'Available backups (sorted by creation date):'
        position = 0
        for file in backups:
            position += 1
            name, ext = os.path.splitext(file)
            f = open(os.path.join(src, file), 'r')
            current = _md5sum(f)
            f.close()
            if last == current and file != 'last':
                print ' %s %s (last)' % (position, name)
            else:
                print ' %s %s' % (position, name)                
        selected = prompt('Enter backup number to import: ')
        if not selected.isdigit():
            print 'Please enter a number between 1 and %s\n' % len(backups)
            selected = None
        elif int(selected) < 0 or int(selected) > len(backups):
            print 'Please enter a number between 1 and %s\n' % len(backups)
            selected = None
    backup_name = backups[int(selected)-1]
    env.backup = (backup_name, os.path.join(src, backup_name))
    return env.backup

def _md5sum(file):
    """Calculate the md5 checksum of a file-like object without reading its
    whole content in memory.

    >>> from StringIO import StringIO
    >>> md5sum(StringIO('file content to hash'))
    '784406af91dd5a54fbb9c84c2236595a'
    """
    m = hashlib.md5()
    while 1:
        d = file.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def restore():
    '''
    Restore mysql database from sql dump file.
    '''
    name, path = _select_backup()
    mysqlimport(path)

def mysqlimport(src):
    '''
    Run mysql import command
    '''
    require('dbhost')
    require('dbname')
    require('dbuser')
    require('dbpassword')    
    local('mysql --default_character_set=utf8 --host=%s --user=%s --pass="%s" \
          %s < %s'%(env.dbhost, env.dbuser, env.dbpassword, env.dbname, src))

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
