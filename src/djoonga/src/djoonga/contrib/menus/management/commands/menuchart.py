from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import sys
import pickle
from django.core import serializers
from djoonga.contrib.menus.utils import get_menu_tree

class Command(BaseCommand):
    help = "Generate a menu chart"
    args = '[optional output]'

    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = False

    def handle(self, output='', *args, **options):
        
        tree = get_menu_tree()
        print tree.dump()
        fp = file('output.pickle', 'w')
        pickle.dump(tree, fp)