from __future__ import with_statement
import os.path
import string
import subprocess
import random
import os
import sys
import fnmatch
import shutil
from git import Repo, Diff
from fabric.api import prompt, put, run, abort, require, env, show, hide, local, abort
from fabric.context_managers import settings, cd
from fabric.contrib.console import confirm
from fabric.contrib.files import append
from ConfigParser import RawConfigParser
from os.path import join, exists, splitext
from djoonga.deployment.db import patch as dbpatch
from djoonga.deployment.utils import md5sum

def deploy():
    '''
    Deploy a branch to remote server.
    1. Prompt to select branch
    2. Generate patch difference between branch and master
    3. Split patch into binary and text branch
    # TODO: Generate sql migration script
    4. Upload patch to server
    5. Dryrun the patch
    6. Apply patch
    7. Perform actions on binary files
    '''
    patch = generate()
    apply(patch)


def generate():
    '''
    Generate patch for specific branch.
    '''
    repo = Repo('.')

    if repo.is_dirty:
        abort('Working tree is dirty. Working tree must be clean to perform this operation.')

    if confirm('Use master as base?'):
        for branch in repo.branches:
            if branch.name == 'master':
                master = branch
    else:
        branch, master = prompt_branch_select(repo, 'Select base branch')

    name, selected_branch = prompt_branch_select(repo)

    while exists(path(name)):
        name = prompt('Directory already exists: %s.\nWhat should I call this patch?'%path(name))

    os.mkdir(path(name))

    rawpath = join(path(name), 'raw.diff')
    local('git diff --binary %s %s > %s'%(selected_branch.commit, master.commit, rawpath))

    with open(rawpath, 'r') as raw:
        changed = raw.read()

    config = RawConfigParser()
    config.add_section('target')
    config.add_section('iteration')
    config.set('target', 'branch', master.name)
    config.set('target', 'commit', master.commit)
    config.set('iteration', 'branch', selected_branch.name)
    config.set('iteration', 'commit', selected_branch.commit)

    print("Generated %s patch directory."%name)

    diffs = Diff.list_from_string(repo, changed)

    def filter(diff):
        def match(pattern):
            if fnmatch.fnmatch(diff.b_path, pattern):
                return pattern
        matches = [match for match in map(match, patterns) if not match is None]
        if not bool(matches):
            return diff

    ignore = os.path.join(os.getcwd(), '.diffignore')
    if os.path.exists(ignore):
        patterns = open(ignore, 'r').read().split('\n')
        diffs = [diff for diff in map(filter, diffs) if not diff is None]

    binary_ext = ['.png', '.gif', '.jpg', '.jpeg', '.flv', '.swf','.zip', '.gz', '.rar', '.fla']

    # TODO: change this to use git generated binary marker
    binaries = [diff for diff in diffs if splitext(diff.b_path)[1] in binary_ext]
    text = set(diffs) - set(binaries)

    config.add_section('patch')
    config.set('patch', 'binary', int(len(binaries) > 0))
    config.set('patch', 'text', int(len(text) > 0))

    print 'Generated patch config file'

    if text:
        text_patch = join(path(name), 'text.patch')
        with open(text_patch, 'w') as pf:
            for diff in text:
                pf.write('%s\n\n'%diff.diff)
        print 'Generated %s text patch'%name
    else:
        text_patch = None

    if binaries:
        binary_list = join(path(name), 'binary.changes')
        binary_base = join(path(name), 'binaries')
        os.mkdir(binary_base)
        with open(binary_list, 'w') as pf:
            for binary in binaries:
                def mkdirs(path):
                    path = join(binary_base, path)
                    try:
                        os.makedirs(path)
                    except:
                        pass
                    return path
                def extractfile(commit, path):
                    dirs, file = os.path.split(path)
                    dirs = mkdirs('%s/%s'%(commit, dirs))
                    with settings(show('stdout'), warn_only = True):
                        if commit == 'target':
                            commit_id = master.commit
                        else:
                            commit_id = selected_branch.commit
                        get_file(commit_id, path, join(binary_base, commit, path))
                if binary.a_commit is None:
                    # new file is being created
                    extractfile('iteration', binary.b_path)
                elif binary.b_commit is None:
                    # file is being removed
                    extractfile('target', binary.a_path)
                else:
                    # file is being updated or renamed
                    extractfile('target', binary.a_path)
                    extractfile('iteration', binary.b_path)

                if binary.new_file:
                    pf.write('new %s\n'%binary.b_path)
                elif binary.deleted_file:
                    pf.write('rm %s\n'%binary.b_path)
                elif binary.renamed:
                    pf.write('mv %s %s\n'%(binary.a_path, binary.b_path))
                else:
                    pf.write('up %s\n'%binary.b_path)
                    
        print 'Generated %s'%binary_list
    else:
        binary_list = None

    with open(join(path(name), 'patch.cfg'), 'wb') as configfile:
        config.write(configfile)

    os.mkdir(join(path(name), 'db'))
    source = join(path(name), 'db', 'source.sql')
    target = join(path(name), 'db', 'target.sql')
    get_file(selected_branch.commit, join('db', 'last'), source)
    get_file(master.commit, join('db', 'last'), target)
    with open(join(path(name), 'db', 'source.sql'), 'r') as sfp:
        with open(join(path(name), 'db', 'target.sql'), 'r') as tfp:
            dbchanged = md5sum(sfp) != md5sum(tfp)
    if dbchanged and confirm('Generate database patch?'):
        dbpatch.generate(join(path(name), 'db'), source, target)
    else:
        shutil.rmtree(join(path(name), 'db'), ignore_errors=True)
        config.set('patch', 'schema', 0)
        config.set('patch', 'data', 0)

    with open(join(path(name), 'patch.cfg'), 'wb') as configfile:
        config.write(configfile)

    return name, path(name)

def apply(patch=None):
    '''
    Apply a patch to remove server.
    '''

    if patch is None:
        patch  = prompt_patch_select()

    config = get_config(patch)

    if config.getboolean('patch', 'text') and confirm('Apply text patch?'):
        patch_text(patch)

    if config.getboolean('patch', 'binary'):
        with open(join(path(patch), 'binary.changes'), 'r') as binarylist:
            binaries = binarylist.readlines()
        for line in binaries:
            item = line.strip().split()
            if len(item) < 3:
                item.append('')
            def new(a, b=None):
                base, file = os.path.split(_remote(a))
                run('mkdir -p %s'%base)
                put(_local(patch, 'iteration', a), _remote(a))
            {'rm': lambda a, b=None: run('rm %s'%_remote(a)),
            'new': new,
            'mv': lambda a,b=None: run('mv %s %s'%(_remote(a),_remote(b))),
            'up': lambda a,b=None: put(_local(patch, 'iteration', a), _remote(b))
            }[item[0]](item[1], item[2])

def reverse(patch=None):
    '''
    Select patch and reverse it on remote server
    '''

    if patch is None:
        patch = prompt_patch_select()

    config = get_config(patch)

    if config.get('patch', 'binary') and confirm('Reverse binary patch?'):
        with open(join(path(patch), 'binary.changes'), 'r') as binarylist:
            binaries = binarylist.readlines()

        for line in binaries:
            item = line.strip().split()
            if len(item) < 3:
                item.append('')
            {'rm':lambda a, b=None: put(_local(patch, 'target', a), _remote(a)),
            'new':lambda a, b=None: run('rm %s'%_remote(a)),
            'mv':lambda a,b=None: run('mv %s %s'%(_remote(b),_remote(a))),
            'up':lambda a,b=None: put(_local(patch, 'target', a), _remote(a))
            }[item[0]](item[1], item[2])

    if config.get('patch', 'binary') and confirm('Reverse text patch?'):
        patch_text(patch, True)

# ----------------- Helper Functions ------------------ #

def patch_text(patch, reverse=False):
    '''Apply text patch to remote server.'''

    def cmd(reverse, dry, path):
        cmd = ['patch']
        if dry: cmd.append('--dry-run')
        if reverse: cmd.append('-R')
        cmd.append('-p1')
        cmd.append('<')
        cmd.append(path)
        return ' '.join(cmd)

    require('base')
    remotep = _remote('%s.patch'%patch)
    put(join(path(patch), 'text.patch'), remotep)
    if confirm('Dry run patch?'):
        with settings(show('stdout'), warn_only = True):
            with cd(env.base):
                run(cmd(reverse, True, remotep))
    if confirm('Execute patch?'):
        with settings(show('stdout'), warn_only = True):
            with cd(env.base):
                run(cmd(reverse, False, remotep))
                log('Applied text patch: %s'%patch)
                run('mv %s patches'%remotep)

def prompt_branch_select(repo, question='What branch should I generate a patch for?'):
    '''
    Ask user to select a branch
    '''
    repo = Repo('.')
    selection = None
    while selection is None:
        print 'Available branches:'
        for branch in repo.branches:
            print ' * %s' % branch.name
        name = prompt(question)
        for branch in repo.branches:
            if name == branch.name:
                selection = branch
        if selection is None:
            print '%s is not a valid branch'%name
    return name, selection

def get_file(commit, source, output):
    '''
    Get contents of a file at source from specific content and copy it to output
    '''
    local('git show %s:%s > %s'%(commit, source, output))

def prompt_patch_select(intro='Available Patches'):
    '''
    Display a list of available patches in specified directory and prompt user to select
    a patch by entering it's number in the list.
    '''
    selected = None
    while selected is None:
        print intro
        pos = 0
        patches = [d for d in os.listdir(path('')) if os.path.isdir(path(d))]
        for patch in patches:
            pos += 1
            print ' %s - %s'%(pos, patch)
        input = prompt("Enter patch number: ")
        if input:
            def valid(input):
                if not input.isdigit():
                    print '%s is not numeric'
                    return False
                if not int(input)-1 in range(0, len(patches)):
                    print '%s is not a valid patch number' % str(int(input)-1)
                    return False
                return True
            if valid(input):
                selected = patches[int(input)-1]
                print 'Selected %s'%selected

    return selected

def path(name):
    '''
    Returns path to patch directory of patch
    '''
    return join(os.getcwd(), 'patches', name.lower())

def _remote(path):
    '''
    Returns path on remote server
    '''
    require('base')
    return join(env.base, path)

def _local(patch, commit, location):
    '''
    Returns path of binary from patch's binaries directory
    '''
    return join(path(patch), 'binaries', commit, location)

def get_config(patch):
    '''
    Get config file for a patch
    '''
    config = RawConfigParser()
    with open(join(path(patch), 'patch.cfg'), 'r') as configfp:
        config.readfp(configfp)
    return config

def log(msg):
    '''
    Adds entry to patch history on remote server
    '''
    with settings(hide('everything'), warn_only = True):
        date = run('date')
        append('%s - %s'%(date, msg), '%s/%s'%(env.base,'.patch_history'))