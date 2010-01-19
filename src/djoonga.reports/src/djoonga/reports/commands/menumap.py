import os
from scrapy.command import ScrapyCommand

class Command(ScrapyCommand):

    requires_project = False

    def syntax(self):
        return "[options]"

    def short_desc(self):
        return "Generate a Chart Map of Menu and Menu Item Relationships"

    def long_desc(self):
        return '''Generate a Chart Map of Menu and Menu Item Relationships'''
        
    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option('-o', "--output", dest="output",
            help="Output path")
        parser.add_option('-t', "--test", dest="test", action="store_true",
            help="Run dependancies test for this command.")
    
    def test(self):
        '''
        Test for dependancies for this script
        '''
        try:
            import AppKit
        except ImportError:
            print "AppKit is not installed. run 'sudo port install py25-pyobjc-cocoa'"
        else:
            print "All system level dependancies are present."
    
    def run(self, args, opts):
        if opts.test:
            self.test()
            exit()
        
        from djoonga.contrib.menus.models import JMenu, JMenuItem
        
        
        