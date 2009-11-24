.. _cli

============================
Command Line Interface (Cli)
============================
Cli is probably one the most powerful tools that you as a developer can have in
your arsenal. When you're working with Djoonga, you will be working in Cli.

When you are running Cli on `*nix` operating systems like Unix, Linux or Mac OS X,
you are operating in a `shell`_. There are different Cli shell interfaces (ie.
`bash`_, `sh`_, `zsh`_)

.. _shell: http://en.wikipedia.org/wiki/Shell_(computing)
.. _bash: http://en.wikipedia.org/wiki/Bourne-Again_shell
.. _sh: http://en.wikipedia.org/wiki/Bourne_shell
.. _zsh: http://en.wikipedia.org/wiki/Z_shell

You can find out what shell you are running by executing ::

echo $SHELL

To understand bash, you need to know that executing bash commands is like
programming by executing 1 line at a time. Same commands can be combined into
scripts to perform multiple operations via one command.

For example, to download Joomla 1.5.15 you would execute the following command ::

wget http://joomlacode.org/gf/download/frsrelease/11396/45609/Joomla_1.5.15-Stable-Full_Package.tar.gz

To extract the contents of the file ::

tar zxvf Joomla_1.5.15-Stable-Full_Package.tar.gz

You can combine both of these commands into 1 script, getjoomla.sh ::

#!/bin/bash
wget http://joomlacode.org/gf/download/frsrelease/11396/45609/Joomla_1.5.15-Stable-Full_Package.tar.gz
tar zxvf Joomla_1.5.15-Stable-Full_Package.tar.gz

if you run ::
./getjoomla.sh

bash will execute both of these commands at the same time.
