# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="taras"
__date__ ="$Feb 1, 2010 10:43:12 AM$"

import hashlib

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