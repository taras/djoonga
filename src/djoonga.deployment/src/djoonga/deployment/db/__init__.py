from __future__ import with_statement
__author__="taras"
__date__ ="$Jan 16, 2010 6:03:31 PM$"

import os
import hashlib
import random
import string

from tempfile import mkdtemp
from datetime import datetime

from fabric.api import run, get, local, prompt, require, env, hosts, abort, hide
from fabric.contrib.console import confirm
from fabric.context_managers import settings

from djoonga.utils.decorators import deprecated
from djoonga.utils import jconfig

from djoonga.deployment.utils import md5sum

def configure():
    '''
    Get database configurations from joomla config file and load them into
    env
    '''
    require('configuration')
    config = jconfig(path=_download_to_tmp(env.configuration))
    env.dbname = config.db
    env.dbuser = config.user
    env.dbpass = config.password
    env.dbhost = config.host

def get_settings(host=None, name=None, user=None, password=None):
    '''
    Get settings from env or from parameters. Parameter settings get priority
    '''
    if host is None:
        require('dbhost')
        host = env.dbhost
    if name is None:
        require('dbname')
        name = env.dbname
    if user is None:
        require('dbuser')
        user = env.dbuser
    if password is None:
        require('dbpass')
        password = env.dbpass
    return host, name, user, password

def schema():
    '''
    Environment setting function to enable only schema export.
    Use this comamnd before restore command if you do not want to export data.
    '''
    env.schema_only = True

def data():
    '''
    Environment settings function to enable only data export
    Use this command before restore command if you do not want to export schema.
    '''
    env.data_only = True

def xml():
    '''
    Environment settings functions to enable xml export
    '''
    env.xml = True

def mysqldump(host=None, name=None, user=None, password=None):
    '''
    Run mysqldump and return the result
    '''

    if hasattr(env, 'schema_only') and env.schema_only:
        export = '--no-data'
    elif hasattr(env, 'data_only') and env.data_only:
        export = '--no-create-info'
    else:
        export = ''
    if hasattr(env, 'xml') and env.xml:
        export ='%s %s'%(export, '--xml')

    host, name, user, password = get_settings(host=host, name=name, user=user, password=password)
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        dump = run('mysqldump --host=%s --user=%s --password=%s %s --quick \
               --lock-tables --add-drop-table %s'% \
               (host, user, password, name, export))
    return dump

def last():
    '''
    Set backup name to 'last'
    '''
    env.last = True

def _prompt_for_backup_name(base_path='db', ext='.sql'):
    '''
    Prompts for new backup name. Verifies that existing file with same name does
    not exist. Returns ( backup_name, backup_path )
    '''
    backup_name = ''
    while not backup_name:
        backup_name = prompt('What should I name this backup?')
        backup_name = backup_name.lower().replace(' ', '_')
        backup_path = os.path.join(base_path, '%s%s'%(backup_name, ext))
        if not backup_name:
            print 'Backup name must not be empty.'
        elif os.path.exists(backup_path):
            backup_name = ''
            print 'Backup file name %s already exists.'%backup_path
            print 'Please, enter another backup name.'
    return backup_name, backup_path

def backup():
    '''
    Backups mysql database on remote server.
    Downloads the backup and places it in db/backups directory
    Sets db/last symbolic link to point to backup file.
    '''
    env.backup = backup_name, backup_path = _prompt_for_backup_name()

    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        output = mysqldump()
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
        last = md5sum(f)
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
            current = md5sum(f)
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

def restore(src=None, host=None, name=None, user=None, password=None):
    '''
    Restore mysql database from sql dump file.
    '''
    if src is None:
        if hasattr(env, 'last') and env.last:
            backup_name, src = 'last', 'db/last'
        else:
            backup_name, src = _select_backup()
    mysqlimport(src, host=host, name=name, user=user, password=password)

def mysqlimport(src, host=None, name=None, user=None, password=None):
    '''
    Run mysql import command
    '''
    host, name, user, password = get_settings(host=host, name=name, user=user, password=password)
    local('mysql --default_character_set=utf8 --host=%s --user=%s --pass="%s" \
          %s < %s'%(host, user, password, name, src))

def _download_to_tmp(src):
    '''
    Downloads contents of file to tmp file. File exists until it's deleted.
    '''
    tmp = mkdtemp()
    name = hashlib.md5(str(datetime.now())).hexdigest()
    dest = os.path.join(tmp, name)
    get(src, dest)
    return dest

def create(name, host=None, user=None, password=None):
    '''
    Create database
    '''
    return execute('create database %s'%name, host=host, user=user, password=password)

def drop(name, host=None, user=None, password=None):
    '''
    Drop database
    '''
    return execute('drop database %s'%name, host=host, user=user, password=password)

def execute(query, host=None, name=None, user=None, password=None):
    '''
    Execute mysql query
    '''
    host, name, user, password = get_settings(host=host, name=name, user=user, password=password)
    return run("mysql --host='%s' --user='%s' --password='%s' -e '%s';"\
        %(host, user, password, query))

def get_tables(name):
    '''
    Return list of tables in specified database
    '''
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        tables = execute("show tables in %s"%name)

    return tables.split('\n')[1:-1]


def select_tables(name):
    '''
    Prompt user to select list of tables from database
    '''
    tables = get_tables(name)
    
    selected = []
    agreed = False
    while not agreed:
        print 'Available tables:'
        pos = 0
        for table in tables:
            pos += 1
            print '%s. %s' % (str(pos), table)
        print 'Select tables to sync by typing in numbers corresponding to the table, seperated by space.'
        input = prompt('Leave line empty for all tables')

        if input:
            def valid(input):
                input = input.split()
                for n in input:
                    if not n.isdigit():
                        print '%s is not numberic'
                        return False
                    if not int(n)-1 in range(0, len(tables)):
                        print '%s is not a valid table number' % str(int(n)-1)
                        return False
                return True
            if valid(input):
                input = input.split()
                for n in input:
                    selected.append(tables[int(n)-1])
                agreed = confirm('Sync the following tables: %s'%' '.join(selected))
        else:
            agreed = confirm('Sync all tables')
            selected = tables

    return selected

def create_test_db():
    '''
    Create a test db and return it's name
    '''
    random.seed()
    name = 'test_%s'%str(random.getrandbits(128))[0:8]
    create(name)
    return name

def sync(source=None, target=None):
    '''
    Generated script will make target same as source

    This can be used to generate a database patch to sync development changes
    to live server
    '''

    if not source is None and not os.path.exists(source):
        print '%s does not exist'%source
        source = None

    if source is None:
        print 'Select source backup:'
        source_name, source_path = _select_backup()

    if not source is None and not os.path.exists(target):
        print '%s does not exist'%target
        target = None

    if target is None:
        print 'Select target backup:'
        target_name, target_source = _select_backup()

    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        tdb = create_test_db()
        sdb = create_test_db()
        restore(target_source, name=tdb)
        restore(source_path, name=sdb)

    if not os.path.exists('db'):
        print 'patches directory does not exist.'
        if confirm('Should I create patches directory in current directory (%s)'\
                   %os.path.join(os.getcwd(), 'db')):
            os.mkdir('db')
        else:
            abort('db directory is required for this operation.')

    patch_name, patch_path = _prompt_for_backup_name(base_path='db', ext='.patch.sql')

    tables = select_tables(sdb)

    t = string.Template("mk-table-sync --print --replace --algorithm=GroupBy \
                        h=$sh,u=$su,p=$sp,D=$sd,t=$table \
                        h=$th,u=$tu,p=$tp,D=$td,t=$table | sed s/'`$td`.'/''/g \
                        >> $output")
    vars = {
        'sh': env.dbhost,
        'th': env.dbhost,
        'su': env.dbuser,
        'tu': env.dbuser,
        'sp': env.dbpass,
        'tp': env.dbpass,
        'sd': sdb,
        'td': tdb,
        'output': os.path.join(os.getcwd(), patch_path)
        }

    patch = file(patch_path, 'a+')
    for table in tables:
            vars['table'] = table
            cmd = t.substitute(vars)
            with settings(warn_only=True):
                run(cmd)
    patch.close()

    print '%s was created'%patch_path

    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        drop(sdb)
        drop(tdb)

@deprecated
def _set_db_settings():
    '''
    Load db settings
    '''
    require('configuration')
    config = jconfig(path=_download_to_tmp(env.configuration))
    env.dbname = config.db
    env.dbuser = config.user
    env.dbpass = config.password
    env.dbhost = config.host