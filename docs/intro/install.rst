.. _intro_install:

==================
Installation Guide
==================
`Djoonga` is written in `Python` and requires `Python` to run.
You need to have `Python` installed before you can install `Djoonga`.

Install Python
==============

Here are some resources to help you install Python on your system

On Windows:
    Python Installation on Windows XP for Newbies
        * `Part 1`_ 
        * `Part 2`_

.. _Part 1: http://showmedo.com/videos/video?name=pythonOzsvaldPyNewbie1&fromSeriesID=49
.. _Part 2: http://showmedo.com/videos/video?name=pythonOzsvaldPyNewbie2&fromSeriesID=49

On Ubuntu:
    Hardy comes with 2.5.2
    Intrepid comes with 2.5.2
    Jaunty comes with 2.6.2rc1
    In conclusion, Ubuntu comes with Python out of the box, so no need to install it.

On Mac OS X:
    Mac OS X comes with a built in version of Python, but I would recommend that
    you install a version of Python through Macports.
    Read `Macports Installation Documentation`_ before installing Macports.
    Follow instructions in 2.3.1 Mac OS X Package Install to install Macports.

.. _Macports Installation Documentation: http://guide.macports.org/#installing

Install setuptools
==================

Once you installed Python, you should install `setuptools` which will provide
you with easy_install. `setuptools` is a Python package that makes it easy to
install other python packages, such as Djoonga.

On Windows
    `Installing easy_install with ez_setup.py`_

.. _Installing easy_install with ez_setup.py: http://showmedo.com/videotutorials/video?name=2070000&fromSeriesID=207

On Ubuntu ::

    sudo apt-get install python-setuptools

On Mac OS X ::
    
    sudo port install py25-setuptools

Install Djoonga
===============

Once `setuptools` is installed, installing Djoonga is easy.

On Windows ::

    easy_install.exe djoonga

On Ubuntu ::

    sudo easy_install djoonga

On Mac OS X ::

    sudo easy_install djoonga

