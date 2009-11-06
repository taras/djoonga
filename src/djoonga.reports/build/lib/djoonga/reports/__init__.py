def main():
	import os
	os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'djoonga.reports.settings')

	from scrapy.command.cmdline import execute
	execute()
