from __future__ import with_statement

__author__="taras"
__date__ ="$Feb 1, 2010 10:43:12 AM$"

import hashlib
import tempfile
import tarfile
import os

def md5sum(file):
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

def cput(name, src, dest):
    '''
    Compress a local file, upload it to remote server and decompress on remote server.
    '''
    tmp = tempfile.NamedTemporaryFile('w+b')
    tmpbase, hashname = os.path.split(tmp)

    destbase, destname = os.path.split(dest)

    tar = tarfile.TarFile(fileobj=tmp)
    patch = '%s.patch'%name
    tarinfo = tarfile.TarInfo(name=patch)
    with open(src, 'r') as patchfile:
        tarinfo.size = len(patchfile.read())
        patchfile.seek(0)
        tar.addfile(tarinfo=tarinfo, fileobj=patchfile)
    tar.close()
    put(tmp, '%s/%s'%(destbase, hashname))


