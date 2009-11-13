.. _tutorial

==================================
Add Djoonga to an Existing Project
==================================

* This tutorial will show you how to add Django to an existing Joomla website.
* This tutorial assumes that Djoonga is installed on your development machine.

Let's say you a very famous developer and you created website for TV show
Crime Scene Investigation and you used csi arconym as the project name.

The project files are located on your computer in **~/Sites/csi**.

If you run ::

    ls -l ~/Sites/csi
    -rw-r--r--   1 taras  staff  97981 Nov  4 12:44 CHANGELOG.php
    -rw-r--r--   1 taras  staff   1175 Nov  4 12:44 COPYRIGHT.php
    -rw-r--r--   1 taras  staff  14894 Nov  4 12:44 CREDITS.php
    -rw-r--r--   1 taras  staff   4344 Nov  4 12:44 INSTALL.php
    -rw-r--r--   1 taras  staff  17816 Nov  4 12:45 LICENSE.php
    -rw-r--r--   1 taras  staff  27984 Nov  4 12:45 LICENSES.php
    drwxr-xr-x  11 taras  staff    476 Nov  4 12:45 administrator
    drwxr-xr-x   2 taras  staff    102 Nov  4 12:46 cache
    drwxr-xr-x  13 taras  staff    476 Nov  4 12:46 components
    -rw-r--r--   1 taras  staff   3409 Nov  4 12:44 configuration.php    
    -rw-r--r--   1 taras  staff   3409 Nov  4 12:44 configuration.php-dist
    -rw-r--r--   1 taras  staff   2771 Nov  4 12:44 htaccess.txt
    drwxr-xr-x   6 taras  staff    986 Nov  4 12:46 images
    drwxr-xr-x   8 taras  staff    918 Nov  4 12:46 includes
    -rw-r--r--   1 taras  staff   2052 Nov  4 12:44 index.php
    -rw-r--r--   1 taras  staff    591 Nov  4 12:44 index2.php
    drwxr-xr-x   4 taras  staff    170 Nov  4 12:45 language
    drwxr-xr-x  16 taras  staff    612 Nov  4 12:46 libraries
    drwxr-xr-x   2 taras  staff    102 Nov  4 12:45 logs
    drwxr-xr-x   3 taras  staff    136 Nov  4 12:46 media
    drwxr-xr-x  22 taras  staff    782 Nov  4 12:46 modules
    drwxr-xr-x  11 taras  staff    408 Nov  4 12:46 plugins
    -rw-r--r--   1 taras  staff    304 Nov  4 12:45 robots.txt
    drwxr-xr-x   6 taras  staff    238 Nov  4 12:46 templates
    drwxr-xr-x   2 taras  staff    102 Nov  4 12:46 tmp
    drwxr-xr-x   4 taras  staff    204 Nov  4 12:46 xmlrpc
    
Restructure
===========

Before we start using Djoonga, we're going to Djoongafy this project. You can
read more about Djoonga project layout on the :doc:`../basics/project_layout` page.

First, let move all Joomla! files into **html** directory::

    mv ~/Sites/csi ~/Sites/html
    mkdir ~/Sites/csi
    mv ~/Sites/html ~/Sites/csi

Now all of the files are conviniently located in **html** directory.

Initialize
==========

Next, let's initialize Djoonga project inside of your project directory.::

    # cd ~/Sites/csi
    # djoonga-admin.py init
    # Install Joomla!? (Y/n) : n
    # Enter path to configuration.php (html/configuration.php):
    Created admin/__init_.py
    Created admin/urls.py
    Created admin/settings.py
    Created admin/development.py
    Created admin/production.py
    Created buildout.cfg
    Created fabfile.py

djoonga-admin's init command creates **admin** directory inside of your project
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

Buildout of the project creates executables that you can use to manage your
Djoonga. ::

    djoonga-admin.py bootstrap development
    Created bin/
    Created eggs/
    Created develop-eggs/
    Created parts/
    Downloaded dependacies
    Created bin/manage
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