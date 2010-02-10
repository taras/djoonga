from __future__ import with_statement
__author__="taras"
__date__ ="$Jan 31, 2010 9:47:53 PM$"

import string

from fabric.api import prompt, put, run, abort, require, env, show, hide, local, abort
from fabric.context_managers import settings, cd
from fabric.contrib.console import confirm
from fabric.contrib.files import append

from djoonga.deployment.db import create_test_db, get_settings, drop, restore, get_tables
from os.path import join, exists, splitext
from schemasync.schemasync import app as generator
from fabric.contrib.files import sed, first

def generate(output, source, target):
    '''
    Generate db syncronization scripts into 'output' directory from source and
    target database file.
    '''
    host, name, user, password = get_settings()
    sdb = create_test_db()
    tdb = create_test_db()
    restore(source, name=sdb)
    restore(target, name=tdb)
    errors = generator(output_directory=output, fpattern=lambda x, tag=None, date_format=None: ('schema.patch.sql', 'schema.reverse.sql'),
                sourcedb='mysql://%s:%s@%s/%s'%(user, password, host, sdb),\
                targetdb='mysql://%s:%s@%s/%s'%(user, password, host, tdb))
    drop(sdb)
    drop(tdb)

    # remove USE query from patches
    sed(join(output, 'schema.patch.sql'), '^USE `%s`;$'%tdb, '')
    sed(join(output, 'schema.reverse.sql'), '^USE `%s`;$'%tdb, '')

    # generate database sync script
    tmp = create_test_db()

    # apply schema changes to test database
    restore(join(output, 'schema.patch.sql'), name=tmp)

    def sync(source, target, output):

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
            'sd': source,
            'td': target
            }

        ignoresource = first(join(output, '.dbignore'), join(os.environ['HOME'], '.dbignore'))
        if not ignoresource is None:
            with open(ignoresource, 'r') as itf:
                ignoretables = [table for table in itf.readlines() if table.strip() == '']

        tables = get_tables(source)
        for table in tables:
            if not table in ignoretables:
                vars['table'] = target
                vars['output'] = output
                cmd = t.substitute(vars)
                with settings(warn_only=True):
                    run(cmd)

    # generate patch from source to temp
    sync(sdb, tmp, join(output, 'data.patch.sql'))
    # generate patch from 


    patch.close()

    if errors == 0:
        print 'Succefully generated db schema migration patches'
    else:
        print 'Errors occured, while generating patches'
