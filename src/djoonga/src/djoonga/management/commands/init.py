from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import sys

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--install-joomla', action='store_false', dest='install_joomla', default=True,
            help='Tells Djoonga to install Joomla! for new project.'),
        make_option('--dbhost', dest='dbhost', default='localhost',
            help='Specifies the database host name'),
        make_option('--dbname', dest='dbname', default='',
            help='Specifies the database name'),
        make_option('--dbuser', dest='dbuser', default='root',
            help='Specifies the database username'),
        make_option('--dbpass', dest='dbpass', default='',
            help='Specifies the database password'),
        make_option('--dbport', dest='dbport', default='3306',
            help='Specifies the database port'),
        make_option('--prepopulate', dest='prepopulate', default=False,
            help='Tells Djoonga to prepopulate new project db with Joomla! demo content.'),
        make_option('--create-vhost', dest='create_vhost', default=True,
            help='Tells Djoonga to create virtualhost for this project.'),
        make_option('--vhost', dest='vhost',
            help='Specifies virtualhost for this project.'),
        make_option('--create-fabfile', dest='create_fabfile', default=True,
            help='Tells Djoonga to create fabfile for this project.'),        
    )
    help = "Initialize Djoonga project inside of current directory."
    args = '<name>'

    def handle(self, name, **options):
        import django

        if not name:
            raise CommandError('Usage is runserver %s' % self.args)

