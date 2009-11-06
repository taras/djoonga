# -*- coding: utf8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from djoonga.reports.items import URLItem
from scrapy.contrib.loader import XPathItemLoader
from urlparse import urlparse, urlunparse, urlsplit
from scrapy.http import Request
import os

class URLAnalysisSpider(CrawlSpider):
    
    # this value needs to be overwritten before spider is used
    domain_name = None
    
    handle_httpstatus_list = [ 200, 404, 500 ]
    
    default_extractor = SgmlLinkExtractor(tags=['a','img'], attrs=['src', 'href'], \
             unique=False, canonicalize=True)
    
    def start_requests(self):
        
        requests = []
        for url in self.start_urls:
            requests.append(Request(url, callback=self.parse,\
                                    meta={'link_title':'',\
                                          'start_url':'true'}))
        
        return requests

    def parse(self, response):
        '''
        Callback function for start_request urls
        '''
        
        items = []
        # store current page
        item = URLItem()
        if response.request.headers.has_key("Referer"):
            item['source'] = str(response.request.headers["Referer"])
        else:
            item['source'] = ''
        item['link_title'] = str(response.request.meta['link_title'])
        item['status'] = int(response.status)
        item['url'] = str(response.request.url)
        items.append(item)
        
        # get links
        if hasattr(response, 'encoding') and \
        ( self.local(response.request.url) or response.request.meta['start_url'] == 'true' ):
            links = self.default_extractor.extract_links(response)
            for link in links:
                items.append(Request(link.url, callback=self.parse,\
                                     meta={'link_title':link.text,\
                                           'start_url':'false'}))            
        return items

    def fix(self, url):
        '''Fix and complete the url'''
        
        u = urlparse(str(url))
        
        scheme  = u.scheme
        netloc  = u.netloc
        path    = u.path
        params  = u.params
        query   = u.query
        fragment = u.fragment
        
        # net location is empty
        if not netloc:
            netloc = self.domain_name
        
        # remove www from url
        if 'www.' in u.netloc and ( self.domain_name in u.netloc or \
                                    self.alias(u.netloc) ):
            netloc = self.domain_name
        
        if not u.scheme:
            scheme = 'http'
        
        return str(urlunparse((scheme, netloc, path, params, query, fragment)))

    def local( self, url ):
        '''Verify that url belongs to local domain'''
        
        # if it's empty return false
        if url == '' :
            return False
        
        u = urlsplit(url)
        
        # urls with empty domain are part of this domain
        if not u.netloc:
            return True
        
        # only http or empty scheme qualify
        if u.scheme != 'http' and not u.scheme:
            return False
        
        # check if url domain belongs to this domain or an alias of this domain
        if self.domain_name not in u.netloc and not self.alias(u.netloc) :
            return False
        
        return True
            
    def alias( self, url ):
        ''' Verifies if specified url is an alias '''
        
        for a in self.aliases:
            if a in url:
                return True
        
        return False


SPIDER = URLAnalysisSpider()
