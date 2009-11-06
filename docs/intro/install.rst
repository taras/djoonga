.. _intro_install:

==================
Installation Guide
==================
Djoonga is written in Python and requires python to run.
You need to have python installed before you can install Djoonga.

Install Python
==============

Here are some resources to help you install Python on your system

On Windows:
Python Installation on Windows XP for Newbies
        Part 1: http://showmedo.com/videos/video?name=pythonOzsvaldPyNewbie1&fromSeriesID=49
        Part 2: http://showmedo.com/videos/video?name=pythonOzsvaldPyNewbie2&fromSeriesID=49

On Ubuntu:
        Hardy comes with 2.5.2
        Intrepid comes with 2.5.2
        Jaunty comes with 2.6.2rc1
        Ubuntu comes with Python out of the box, so no need to install it.

On Mac OS X:
Mac OS X comes with a built in version of Python, but I would recommend that you install a version of Python through Macports.
Read Installation Documentation http://guide.macports.org/#installing before installing Macports.
Follow instructions in 2.3.1 Mac OS X Package Install to install Macports.

Install setuptools
==================

Once you installed Python, you should install setuptools which will provide you with easy_install .
setuptools is a Python package that makes it easy to install other python packages, such as Djoonga.

On Windows:
        Installing easy_install with ez_setup.py - http://showmedo.com/videotutorials/video?name=2070000&fromSeriesID=207

On Ubuntu:
        To install easy_install run 'sudo apt-get install python-setuptools'

On Mac OS X:
        To install easy_install with macports run 'sudo port install py25-setuptools'

Install Djoonga
===============

Once setuptools are installed, installing Djoonga is easy.

On Windows:
        run 'easy_install.exe djoonga'

On Ubuntu:
        run 'easy_install djoonga'

On Mac OS X
        run 'easy_install djoonga'

