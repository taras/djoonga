.. _new_project

=====================================
Setup new Joomla project with Djoonga
=====================================
This tutorial will show you how to setup a new Joomla project with Djoonga.

For this tutorial you will imagine that you are a very famous developer and you
are creating a website for TV show Crime Scene Investigation. The acronym for
this project will be *csi*.

Initalize
=========

Let's initialize our Djoonga project ::

    # cd ~/Sites
    # djoonga-admin.py init csi
    Created csi directory
    # Install Joomla? (Y/n):
    # Where should I install Joomla!? (html):  
    Created csi/html directory
    # Database name? (csi): 
    # Database host? (localhost): 
    # Database username? (root): 
    # Database password? (): 
    # Database port? (3306): 
    Imported database schema into csi database
    # Prepopulate the database with default Joomla! content? (N/y): 
    # Create virtualhost for this project? (Y/n):
    # What should be the name for this host? (csi):
    Created virtualhost csi
    Created admin/__init_.py
    Created admin/urls.py
    Created admin/settings.py
    Created admin/development.py
    Created admin/production.py
    Created buildout.cfg
    Created fabfile.py

**djoonga-admin init** command creates *admin* directory inside of your project
directory. Let's look closer at what was created.

admin/__init__.py
    Python needs this file to import modules

admin/urls.py
    Djoonga urls module that tells Djoonga about available url patterns.

admin/settings.py
    Settings module that has global configuration that applies to all environments.

admin/development.py
    Extends settings module to add development specific settings.

admin/production.py
    Extends settings module to add production specific settings.

buildout.cfg
    Buildout configuration file that contains all of the Python dependancies.
    Buildout allows you to quickly and easily install all of the Python packages
    that Djoonga depends on. Read more about how :doc:`../tools/buildout`
    is used with Djoonga.
    
fabfile.py
    Fabric configuration file contains information about your servers.
    Fabric is a deployment automation tool that we use to interact with remote
    servers in a secure and efficient manner. Read more about how
    :doc:`../tools/fabric` is used with Djoonga.

Buildout
========

Buildout downloads all of the dependancies for your project and creates
executables for you in bin/ directory. ::

    # djoonga-admin.py buildout development
    Created bin/
    Created eggs/
    Created develop-eggs/
    Created parts/
    Downloaded dependacies
    Created bin/manage.py
    Created bin/fab

Run Server
==========

To start the server, run ::

    bin/manage.py runserver
    
This command will start your Djoonga server.
Now, go to http://localhost:8080 to see your first Djoonga setup.

At this point you should be able to login with your Joomla! Super Administrator
username and password.

You're done!