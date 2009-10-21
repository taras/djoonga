#!/usr/bin/env python
from fabric.api import run, get, local, prompt
from tempfile import mkdtemp

def backup():
    '''
    Backups mysql database on remote server.
    Downloads the backup and places it in db/backups directory
    Sets db/last symbolic link to point to backup file.
    '''
    backup_name = ''
    while not backup_name:
        backup_name = prompt('What should I name this backup?')
        if not ( backup_name and backup_name.isalnum() ):
            print 'Backup name must be atleast 1 character long and be alphanumberic.'
    backup_name = backup_name.lower().replace(' ', '_')
    run('mysqldump --host=%s --user=%s --password=%s %s --quick --lock-tables --add-drop-table > %s')
    
    output = 'db/backups/%s.sql'%backup_name
    get('~/db/db.sql', output)
    #local('ln -s -f %s.sql db/last' % filename)