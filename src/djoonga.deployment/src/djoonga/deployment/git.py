import string, subprocess, random, os
from git import Repo, Diff

def generate_patch():
    '''
    Generate patch for specific branch.
    '''
    repo = Repo('.')
    print 'Available branches:'
    for branch in repo.branches:
        print ' * %s' % branch.name
    branch = prompt('What branch should I generate a patch for?')
    commits = repo.commits(branch)
    changed = local('git diff --no-prefix %s %s'%(commits[-1], commits[0]))

    def path(name):
        return os.path.join('patches','%s.patch'%name.lower().strip(' '))

    patch = branch
    while os.path.exists(path(patch)):
        patch = prompt('%s already exists. What should I call this patch?'%path)
    fp = open(path(patch), 'w')
    fp.writelines(changed)
    fp.close()

def test_patch():
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
        exit()
    remote = os.path.join('~', path)
    put(path, remote)
    run('patch --dry-run -p0 < %s'%remote)
