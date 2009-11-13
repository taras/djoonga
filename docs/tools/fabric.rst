.. _fabric

=============================
Use Fabric to easy deployment
=============================

According to `Fabric's website`_, "Fabric is a Python library and command-line
tool for streamlining the use of `SSH`_ for application deployment or systems
administration tasks."

.. _Fabric's website: http://fabfile.org
.. _SSH: http://en.wikipedia.org/wiki/Secure_Shell

Let's look closer at this statement and what each part of that statement means.

*Python Library*
    Means that you can use Fabric's API to add functionality to your application.

*Command-line tool*
    Means that you can run Fabric through command line.
    
*Streamlining the use of SSH*
    What kind of tasks does it streamline?
        * SSH key handling for authentication on remote servers
        * Execution of scripts on multiple remote servers

*Application Deployment*
    Applications like Joomla!

*System Administration Tasks*
    Such as:
        * Database setup, import and backup
        * File uploading, downloading and patching
    
Why use Fabric?
===============

#. *It's fast*

    Fabric automates repetitive daily tasks such as database backups and imports.
    This can shave off from minutes to hours off your daily tasks. A typical
    backup and import process takes 2-3 seconds from the moment that the developer
    decided to run the backup to the moment that the backup is complete.

#. *It's secure*

    All interaction with remote servers happens through SSH. All SSH communication
    is encrypted which means that no one can snoop on what you're transfering
    through the network.

#. *Public-key authentication (`Public-key cryptopgraphy`_)*

    Public-key authentication allows you to control access to your production
    servers in a way that's not possible with FTP. It gives you the power to
    at any point revoke access to the server without impacting other individuals
    who have access to the server.

#. *Encourages proper deployment process*
    
    In absense of Public-key based authentication, organizations are forced to
    provide developers with access to production servers via ftp. This is a
    major problem from security prospective, because it is impossible to track
    who has access to the ftp server.

.. _Public-key cryptopgraphy: http://en.wikipedia.org/wiki/Public-key_cryptography

How does Fabric work?
=====================
Fabric runs functions from *fabfile.py*.

A typical fabric command would look like this ::

    ./bin/fab live db backup
    
Let's see if you can guess what that command does. You're right, it runs
db backup on remote server.

What about? ::

    ./bin/fab dev db restore

Right again, imports db backup on dev server.

What does a fabfile look like?
==============================

Here is what a typical fabfile looks like. ::

    from __future__ import with_statement
    from fabric.api import env
    from djoonga.deployment.fabfile.db import backup, restore, settings

    def db():
        settings()

    def live():
        env.host_string = 'example.com'
        env.user = 'example'
        env.configuration = '~/public_html/configuration.php'
    
    def dev():
        env.host_string     = 'localhost'
        env.configuration   =  os.path.join(os.getcwd(),'html','configuration.php')

How to write Fabric functions?
==============================
Fabric functions can be very simple or very advanced, depending on what you're
trying to accomplish.

Basic use case is automation of database and file related operations on
remote servers, but Fabric is Python, so a Fabric function can do anything.

Some things to keep in mind:

Fabric was created to simplify interaction with remote server though ssh.
This means that when you're thinking about how to execute system specific
commands, you need to think about weather the functions is going to be executed
locally using *local()*, remotely using *run()* or *sudo()*.

From Fabric's prospective, *run()* and *sudo()* executed on `localhost` is exactly
the same as being executed on remote server. In fact, they're both executed
through ssh. So when you run something like ::

    ./bin/fab dev db backup

You're actually logging in to your localhost through ssh and executing the
command.

To help you grasp this concept in your mind, think:
#. I log into the server
#. I execute command

In the same way, if a command that you're executing is not working, try logging
into the server through ssh and executing this command.

Most common problem that I see with Fabric commands is that the command can not
be executed because the executable can not be found. To solve this, log into
the server through ssh and run ::
    
    which {executable}
    
this will give you the path to the executable, or nothing if it can not be found.

SSH Keys
========
To be able to use Fabric, you need to generate SSH keys. Github has a very good
`tutorial on generating SSH Keys`_.

When creating SSH keys, it is recommended to enter a passphrase that will
protect your private key, incase it falls into the wrong hands. The problem with
passphrases is that they require you to enter it every time that you use your
public key.

The solution to this is called `Keychain`_. Keychain is available on `*nix`
systems like Linux, Unix and Mac OS X.

You can install Keychain on your `*nix` machine via:

Mac OS X ::

    sudo port install keychain

Ubuntu ::

    sudo apt-get install keychain

.. _tutorial on generating SSH Keys: http://github.com/guides/providing-your-ssh-key
.. _Keychain: http://www.gentoo.org/proj/en/keychain/