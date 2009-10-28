import os
from scrapy.command import ScrapyCommand
from scrapy.contrib.exporter import XmlItemExporter, CsvItemExporter
from scrapy.contrib.exporter import PickleItemExporter
from scrapy.contrib.exporter.jsonlines import JsonLinesItemExporter
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from scrapy.core.manager import scrapymanager
from djoonga.reports.spiders.urlanalysis import SPIDER

class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[options] <domain> <output>"

    def short_desc(self):
        return "Run URL analyzer on domain"

    def long_desc(self):
        return '''Run URL analyzer on specified domain and alias domains.
        Output is stored in specified output file in CSV, XLS, XML or JSON
        formats.
        '''
        
    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option('-a', "--alias", dest="alias",
            help="Alias for this domain. You can use this option more then once.")
        parser.add_option('-s', "--start_url", dest="start_url",
            help="Start url for this analysis. You can use this option more then once.")
    
    def run(self, args, opts):
        if len(args) != 2:
            return False
        output = args[1]
        file = open(output, 'w+b')
        root, ext = os.path.splitext(output)
        exporter =  {
            '.json': JsonLinesItemExporter,
            '.xml': XmlItemExporter,
            '.csv': CsvItemExporter,
            '.pickle': PickleItemExporter
            }[ext](file)
        dispatcher.connect(exporter.export_item, signal=signals.item_passed)
        exporter.start_exporting()
        SPIDER.domain_name = args[0]
        if opts.alias == None:
            SPIDER.aliases = []
        else:
            SPIDER.aliases = opts.alias
        if opts.start_url == None:
            SPIDER.start_urls = ['http://%s'%SPIDER.domain_name]
        else:
            SPIDER.start_urls = opts.start_url
        scrapymanager.runonce(SPIDER)
        exporter.finish_exporting()
        