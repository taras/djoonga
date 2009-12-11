from fabric.api import local, abort
from fabric.contrib.console import confirm
from distutils.version import StrictVersion
import hashlib
import os

# what directories or files to exclude from diff?
exclude = ['installation', '.svn']
base = os.path.join('parts', 'joomla')

def _sort(versions):
    '''
    Return a sorted list of Joomla versions
    '''
    
    def find_key(dic, val):
        """return the key of dictionary dic given the value"""
        return [k for k, v in dic.iteritems() if v == val][0]
    
    def find_value(dic, key):
        """return the value of dictionary dic given the key"""
        return dic[key]
    
    class Lookup(dict):
        """
        a dictionary which can lookup value by key, or keys by value
        """
        def __init__(self, items=[]):
            """items can be a list of pair_lists or a dictionary"""
            dict.__init__(self, items)
    
        def get_key(self, value):
            """find the key(s) as a list given a value"""
            return [item[0] for item in self.items() if item[1] == value]
    
        def get_value(self, key):
            """find the value given a key"""
            return self[key]
    
    def translate(v, pos):
        if '.RC' in v:
            return v.replace('.RC', 'a')
        elif 'RC' in v:
            return v.replace('RC', 'a%s'%pos)
        else:
            return v
    
    translated = {}
    pos = 0
    for joomla_version in versions:
        translated[joomla_version] = translate(joomla_version, pos)
        pos =+ 1
    
    strict = []
    for joomla_version, strict_version in translated.items():
        try:
            version = StrictVersion(strict_version)
        except ValueError:
            abort('Could not parse version string: %s'%strict_version)
        else:
            translated[joomla_version] = str(version)
            strict.append(version)
    
    strict.sort()
    sorted = []
    for v in strict:
        sorted.append(find_key(translated, str(v)))
    
    return sorted

def test():
    '''
    Test for requirements
    '''

    # test base_path
    assert base_path('1.5.1') == os.path.join(base, '1.5', '1.5.1'), \
    'Expecting %s, got %s' % (os.path.join(base, '1.5', '1.5.1'), base_path('1.5.1'))
    assert base_path('1.5.0.RC2') == os.path.join(base, '1.5', '1.5.0.RC2'), \
    'Expecting %s, got %s' % (os.path.join(base, '1.5', '1.5.0.RC2'), base_path('1.5.0.RC2'))

    # test diff_cmd
    expect = 'diff -x installation -x .svn %s %s' % (base_path('1.5.0'), base_path('1.5.10'))
    assert diff_cmd('1.5.0', '1.5.10') == expect, 'Expecting %s, got %s'%(diff_cmd('1.5.0', '1.5.10'), expect)

    # test version compare
    versions = ['1.5.0', '1.5.0.RC1', '1.5.0.RC2', '1.5.0.RC3', '1.5.0.RC4', \
                '1.5.1', '1.5.10', '1.5.11', '1.5.12', '1.5.12RC', '1.5.13', \
                '1.5.14', '1.5.15', '1.5.2', '1.5.3', '1.5.4', '1.5.5', '1.5.6',\
                '1.5.7', '1.5.8', '1.5.9']
    sorted = [  '1.5.0.RC1', '1.5.0.RC2', '1.5.0.RC3', '1.5.0.RC4', '1.5.0', \
                '1.5.1', '1.5.2', '1.5.3', '1.5.4', '1.5.5', '1.5.6',\
                '1.5.7', '1.5.8', '1.5.9', '1.5.10', '1.5.11', '1.5.12RC', \
                '1.5.12',  '1.5.13', '1.5.14', '1.5.15']
    assert _sort(versions) == sorted, 'Expected %s, got %s' % (sorted, _sort(versions))

def base_path(version):
    '''
    Return path to the directory of the version in joomla repository
    '''
    return os.path.join(base, version[0:3], version)

def diff_cmd(from_version, to_version):
    '''
    Return command for generating diff between 2 directories from joomla repository
    from_version - from this version diff will be generated (ie. 1.5.0)
    to_version - to this version diff will be generated (ie. 1.5.10)
    '''
    excludes = ''
    for item in exclude:
       excludes = '%s -x %s' % (excludes, item)
    return 'diff %s %s %s'%(excludes, base_path(from_version), base_path(to_version))

def generate_patches(joomla='1.5'):
    '''
    Generate patches for joomla of specific version of joomla
    '''
    source = os.path.join(base, joomla)
    if not os.path.exists(source):
        abort('Files for requested version of Joomla do not exist in %s'%source)
    
    versions = [v for v in os.listdir(source) if v not in exclude]
    sorted = _sort(versions)
    
    last = sorted[-1]
    old = sorted[0:-1]
    old.reverse()
    for v in old:
        print diff_cmd(v, last)
        
def build_latest():
    '''
    Create archive of latest distributions of parts/joomla
    and store them in ../../joomla
    '''
    
    # path to location of tags from joomla svn repository
    joomla_tags = os.path.join('parts','joomla')
    
    # output directory where created files will be stored
    output = os.path.abspath(os.path.join('..','..','joomla'))

    # for each major version generate latest archive
    for major_version in os.listdir(joomla_tags):
        version_dir = os.path.join(joomla_tags, major_version)
        # get list of all versions, exclude .svn
        versions = [v for v in os.listdir(version_dir) if v not in exclude]
        sorted = _sort(versions)
        latest = sorted[-1]
        output_dir = os.path.join(output, major_version)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        latest_output = os.path.join(output, major_version, 'latest.tar.gz')
        source = os.path.join(version_dir, latest)

        # create archive
        local('tar --exclude=.svn --directory=%s -pczf %s .'%(source, latest_output))
        
        # genereate MD5 hash for generated file
        f = open(latest_output, 'rb')
        hash = hashlib.md5()
        hash.update(f.read())
        hash = hash.hexdigest()
        f.close()
        
        f = open(os.path.join(output, major_version, 'CHECKSUM'), 'w')
        f.write(hash)
        f.close()
        
        f = open(os.path.join(output, major_version, 'VERSION'), 'w')
        f.write(latest)
        f.close()
        