import os
from datetime import datetime
from scrapy.command import ScrapyCommand
from scrapy.contrib.exporter import XmlItemExporter, CsvItemExporter
from scrapy.contrib.exporter import PickleItemExporter
from scrapy.contrib.exporter.jsonlines import JsonLinesItemExporter
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from scrapy.core.manager import scrapymanager
from scrapy import log
from djoonga.reports.spiders.urlanalysis import SPIDER
from djoonga.reports.pipelines import ReportJunction

class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[options] <domain> <output>"

    def short_desc(self):
        return "Run URL analyzer on domain"

    def long_desc(self):
        return '''Generate a URL analysis of urls on specified domain and alias domains.
Output is stored in specified in reports directory. Each time the report is ran, a directory
is created in reports directory with 4 files: errors, dirtyurls, offsite and clean.

errors - contains all urls that produced 404 or 500 errors
dirtyruls - contains all urls with 'index.php' in the url
offsite - contains all urls that are not on main domain or alias domain
clean - contains all other urls that are ok'''
        
    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option('-a', "--alias", dest="alias",
            help="Alias for this domain. You can use this option more then once.")
        parser.add_option('-s', "--start_url", dest="start_url",
            help="Start url for this analysis. You can use this option more then once.")
        parser.add_option('-f', "--format", dest="format",
            help="Output formats: json, xml, csv, pickle", default='csv')
        parser.add_option('-o', "--output", dest="output",
            help="Directory to output reports to", default=os.path.join(os.getcwd(), 'reports'))
        parser.add_option('-n', "--name", dest="name",
            help="Name of this report, default: start time", default=datetime.now().strftime('%Y-%m-%d %I:%M:%S'))

    def run(self, args, opts):

        # if not domain argument was given, then exit
        if len(args) == 0:
            return False
        domain = args[0]

        # create directory to store the report output
        path = [opts.output, domain, opts.name]
        parent = ''
        for d in path:
            parent = os.path.join(parent, d)
            if not os.path.exists(parent):
                os.mkdir(parent)
                log.msg('Created directory: %s'%parent, level=log.INFO)

        output = os.path.join(*path)
        reports = ['errors', 'dirtyurls', 'offsite', 'clean']
        
        # create exporter for each report type
        exporters = {}
        for report in reports:
            file = open(os.path.join(output, '%s.%s'%(report, opts.format)), 'w+b')
            exporter =  {
                'json': JsonLinesItemExporter,
                'xml': XmlItemExporter,
                'csv': CsvItemExporter,
                'pickle': PickleItemExporter
                }[opts.format](file)
            exporters[report] = exporter
        junction = ReportJunction(exporters)
        dispatcher.connect(junction, signal=signals.item_passed)
        junction.start()
        SPIDER.domain_name = domain
        if opts.alias == None:
            SPIDER.aliases = []
        else:
            SPIDER.aliases = opts.alias
        if opts.start_url == None:
            SPIDER.start_urls = ['http://%s'%SPIDER.domain_name]
        else:
            SPIDER.start_urls = opts.start_url
        scrapymanager.runonce(SPIDER)
        junction.finish()
        