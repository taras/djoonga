import os
import django.core.management

def production():
    '''
    Run production environment. Default DJOONGA values can be overwritten by
    using system variable. Module format is same as for DJANGO_SETTINGS_MODULE
    '''
    if os.getenv('DJOONGA_PRODUCTION_SETTINGS') is None:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djoonga.conf.production')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJOONGA_PRODUCTION_SETTINGS'))
    django.core.management.execute_from_command_line()

def development():
    '''
    Run development environment. Default DJOONGA values can be overwritten by
    using system variable. Module format is same as for DJANGO_SETTINGS_MODULE
    '''    
    if os.getenv('DJOONGA_DEVELOPMENT_SETTINGS') is None:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djoonga.conf.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJOONGA_DEVELOPMENT_SETTINGS'))
    django.core.management.execute_from_command_line()        