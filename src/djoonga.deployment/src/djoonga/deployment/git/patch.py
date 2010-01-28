from __future__ import with_statement
import os.path
import string
import subprocess
import random
import os
import sys
import fnmatch
from git import Repo, Diff
from fabric.api import prompt, put, run, abort, require, env, show, hide, local
from fabric.context_managers import settings, cd
from fabric.contrib.console import confirm
from fabric.contrib.files import append

def deploy():
    '''
    Deploy a branch to remote server.
    1. Prompt to select branch
    2. Generate patch difference between branch and master
    3. Split patch into binary and text branch
    # TODO: Generate sql migration script
    4. Upload patch to server
    5. Test the patch
    6. Apply patch
    7. Perform actions on binary files
    '''
    branch, patch, path = generate()
    text_patch, binary_list = split(patch, branch.commit)
    apply(text_patch, binary_list)

def prompt_branch_select(repo):
    '''
    Ask user to select a branch
    '''
    repo = Repo('.')
    selection = None
    while selection is None:
        print 'Available branches:'
        for branch in repo.branches:
            print ' * %s' % branch.name
        name = prompt('What branch should I generate a patch for?')
        for branch in repo.branches:
            if name == branch.name:
                selection = branch
        if selection is None:
            print '%s is not a valid branch'%name
    return name, selection

def generate():
    '''
    Generate patch for specific branch.
    '''
    repo = Repo('.')
    name, selected = prompt_branch_select(repo)
    for branch in repo.branches:
        if branch.name == 'master':
            master = branch
    changed = local('git diff --binary %s %s'%(master.commit, selected.commit))

    def path(name):
        return os.path.join('patches','%s.patch'%name.lower().strip(' '))

    patch = name
    while os.path.exists(path(patch)):
        patch = prompt('%s already exists. What should I call this patch?'%path(patch))
    fp = open(path(patch), 'w')
    fp.writelines(changed)
    fp.close()
    return selected, patch, path

def prompt_patch_select(path=os.path.join(os.getcwd(), 'patches'), intro='Available Patches'):
    '''
    Display a list of available patches in specified directory and prompt user to select
    a patch by entering it's number in the list.
    '''
    selected = None
    while selected is None:
        print intro
        pos = 0
        patches = [os.path.splitext(p)[0] for p in os.listdir(path) if os.path.splitext(p)[1] == '.patch']
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
                path = os.path.join(path, '%s.patch'%selected)

    return selected, path

def test():
    '''
    Uploads patch to the server and tests it
    '''
    print 'Available Patches'
    for file in os.listdir('patches'):
        name, ext = os.path.splitext(file)
        if ext == '.patch':
            print ' * %s'%name
    patch = prompt('What patch would you like to test?')
    path = os.path.join('patches','%s.patch'%patch)
    if not path:
        print '%s.patch does not exist in %s'(patch, os.path.abspath('patches'))
        sys.exit()
    remote = os.path.join('~', path)
    put(path, remote)
    run('patch --dry-run -p0 < %s'%remote)

def split(patch=None, commit=None):
    '''
    Select a patch and split it in to 2 patches, one with text file differences
    and one with binary file differences.
    '''
    if patch is None:
        patch, path  = prompt_patch_select()
    else:
        path = os.path.join(os.getcwd(), 'patches', '%s.patch'%patch)
        if not os.path.exists(path):
            patch, path  = prompt_patch_select()

    pf = open(path, 'r')
    patch_text = pf.read()
    pf.close()
    repo = Repo('.')
    diffs = Diff.list_from_string(repo, patch_text)

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

    binary_ext = ['.png', '.gif', '.jpg', '.jpeg', '.flv', '.swf','.zip', '.gz', '.rar']

    # TODO: change this to use git generated binary marker
    binaries = [diff for diff in diffs if os.path.splitext(diff.b_path)[1] in binary_ext]
    text = set(diffs) - set(binaries)

    if text:
        text_patch = os.path.join(os.getcwd(), 'patches', '%s.text.patch'%patch)
        pf = open(text_patch, 'w')
        for diff in text:
            pf.write('%s\n\n'%diff.diff)
        pf.close()
        print 'Generated %s'%text_patch
    else:
        text_patch = None

    if binaries:
        binary_list = os.path.join(os.getcwd(), 'patches', '%s.binaries.list'%patch)
        binary_base = os.path.join(os.getcwd(), 'patches', '%s.binaries'%patch)
        if not os.path.exists(binary_base):
            os.mkdir(binary_base)
        pf = open(binary_list, 'w')
        for binary in binaries:
            if not binary.b_commit is None:
                dirs, file = os.path.split(binary.b_path)
                try:
                    os.makedirs(os.path.join(binary_base, dirs))
                except:
                    pass
                with settings(show('stdout'), warn_only = True):
                    local('git checkout %s %s'%(commit, binary.b_path))
                    local('cp %s %s'%(os.path.join(os.getcwd(), binary.b_path), os.path.join(binary_base, dirs)))
                    local('git reset HEAD %s'%binary.b_path)
            if binary.new_file:
                pf.write('new %s\n'%binary.b_path)
            elif binary.deleted_file:
                pf.write('rm %s\n'%binary.b_path)
            elif binary.renamed:
                pf.write('mv %s %s\n'%(binary.a_path, binary.b_path))
            else:
                pf.write('up %s\n'%binary.b_path)
        pf.close()
        print 'Generated %s'%binary_list
    else:
        binary_list = None

    return text_patch, binary_list

def apply(text=None, binary=None, commit=None):
    '''
    Apply a patch to remove server.
    '''

    if text is None and binary is None:
        patch, path  = prompt_patch_select()

        text = os.path.join(os.getcwd(), 'patches', '%s.text.patch'%patch)
        binary = os.path.join(os.getcwd(), 'patches', '%s.binaries.list'%patch)

    if not os.path.exists(text) and not os.path.exists(binary):
        if prompt('Split patch file into text and binary patches?'):
            text, binary = split(patch=patch)
    else:
        if os.path.exists(text):
            base, text_patch = os.path.split(text)
        else:
            text = None
        if not binary is None and os.path.exists(binary):
            base, binary_list = os.path.split(binary)
        else:
            binary = None

    require('base')
    if not text is None:
        put(text, env.base)
        if confirm('Dry run patch?'):
            with settings(show('stdout'), warn_only = True):
                with cd(env.base):
                    run('patch --dry-run -p1 < %s'%os.path.join(env.base, text_patch))
        if confirm('Execute patch?'):
            with settings(show('stdout'), warn_only = True):
                with cd(env.base):
                    run('patch -p1 < %s'%os.path.join(env.base, text_patch))
                    log('Applied patch: %s'%text_patch)
                    run('mv %s.patch patches'%text_patch)

    if not binary is None:
        binaries = open(binary, 'r').readlines()
        for line in binaries:
            item = line.strip().split()
            if len(item) < 3:
                item.append('')
            {'rm':lambda a, b=None: run('rm %s'%os.path.join(env.base, a)),
            'new':lambda a, b=None: put(os.path.join(os.getcwd(), a), os.path.join(env.base, a)),
            'mv':lambda a,b=None: run('mv %s %s'%(os.path.join(env.base, a),os.path.join(env.base, b))),
            'up':lambda a,b=None: put(os.path.join(os.getcwd(),a), os.path.join(env.base, a))
            }[item[0]](item[1], item[2])

def log(msg):
    '''
    Adds entry to patch history on remote server
    '''
    with settings(hide('everything'), warn_only = True):
        date = run('date')
        append('%s - %s'%(date, msg), '%s/%s'%(env.base,'.patch_history'))

def reverse():
    '''
    Select patch and reverse it on remote server
    '''
    patch, path  = prompt_patch_select()

    require('base')
    put(path, env.base)
    if confirm('Dry run patch?'):
        with settings(show('stdout'), warn_only = True):
            with cd(env.base):
                run('patch --dry-run -R -p1 < %s.patch'%os.path.join(env.base, patch))
    if confirm('Execute patch?'):
        with settings(show('stdout'), warn_only = True):
            with cd(env.base):
                reason = prompt("What's the reason for this action?: ")
                run('patch -R -p1 < %s.patch'%os.path.join(env.base, patch))
                log('Reversed patch: %s because %s'%(patch, reason))
                run('mv %s.patch patches'%patch)
