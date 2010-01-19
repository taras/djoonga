# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log

class ReportJunction(object):
    '''
    Redirect items to the appropriate report based on item type
    '''
    def __init__(self, exporters):
        self.exporters = exporters

    def __call__(self, item):
        if item['reports']:
            for report in item['reports']:
                self.exporters[report].export_item(item)
                log.msg('Added %s to %s'%(item, report), log.INFO)
        else:
            log.msg('%s was not filed'%item, log.ERROR)

    def start(self):
        '''Execute start_exporting on each exporter'''
        for exporter in self.exporters.itervalues():
            exporter.start_exporting()

    def finish(self):
        '''Execute finish_exporting on each exporter'''
        for exporter in self.exporters.itervalues():
            exporter.finish_exporting()

class ReportsPipeline(object):

    def process_item(self, domain, item):
        return item
