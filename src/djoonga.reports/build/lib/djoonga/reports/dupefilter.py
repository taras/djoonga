import weakref
import hashlib
from scrapy.contrib import dupefilter
from scrapy.utils.url import canonicalize_url

_fingerprint_cache = weakref.WeakKeyDictionary()
def request_fingerprint(request, include_headers=None):
    """
    Return the request fingerprint.
    
    This was taken from scrapy.utils, but we added canocalization for Referer url
    
    The request fingerprint is a hash that uniquely identifies the resource the
    request points to. For example, take the following two urls:
    
    http://www.example.com/query?id=111&cat=222
    http://www.example.com/query?cat=222&id=111

    Even though those are two different URLs both point to the same resource
    and are equivalent (ie. they should return the same response).

    Another example are cookies used to store session ids. Suppose the
    following page is only accesible to authenticated users:
    
    http://www.example.com/members/offers.html

    Lot of sites use a cookie to store the session id, which adds a random
    component to the HTTP Request and thus should be ignored when calculating
    the fingerprint. 
    
    For this reason, request headers are ignored by default when calculating
    the fingeprint. If you want to include specific headers use the
    include_headers argument, which is a list of Request headers to include.

    """
    if include_headers:
        include_headers = tuple([h.lower() for h in sorted(include_headers)])
    cache = _fingerprint_cache.setdefault(request, {})
    if include_headers not in cache:
        fp = hashlib.sha1()
        fp.update(request.method)
        fp.update(canonicalize_url(request.url))
        fp.update(request.body or '')
        if include_headers:
            for hdr in include_headers:
                if hdr in request.headers:
                    fp.update(hdr)
                    for v in request.headers.getlist(hdr):
                        if v != '':
                            v = canonicalize_url(v)
                        fp.update(v)
        cache[include_headers] = fp.hexdigest()
    return cache[include_headers]

class RequestRefererDupeFilter(dupefilter.RequestFingerprintDupeFilter):
    '''
    In addition to it's parent's functionality, this filter includes
    Referer in determening if request has been looked at.
    '''
    def request_seen(self, spider, request, dont_record=False):
        if request.headers.has_key("Referer"):
            request.headers['Referer'] = spider.fix(request.headers['Referer'])
        fp = request_fingerprint(request, include_headers=("Referer",))
        if fp in self.fingerprints[spider]:
            return True
        if not dont_record:
            self.fingerprints[spider].add(fp)
        return False