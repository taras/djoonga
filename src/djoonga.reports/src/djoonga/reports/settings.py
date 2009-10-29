# Scrapy settings for reports project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

import djoonga.reports

BOT_NAME = 'djoonga.reports'
BOT_VERSION = '1.0'

SPIDER_MODULES = []
NEWSPIDER_MODULE = 'djoonga.reports.spiders'
DEFAULT_ITEM_CLASS = 'djoonga.reports.items.URLItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
COMMANDS_MODULE = 'djoonga.reports.commands'

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}

DUPEFILTER_CLASS = 'djoonga.reports.dupefilter.RequestRefererDupeFilter'