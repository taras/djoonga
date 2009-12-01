.. _vcs

=======================
Version Control Systems
=======================

If you're not using any `Version Control System`_,VCS, right now, then do yourself a
favour and start using it today.

.. _Version Control System: http://en.wikipedia.org/wiki/Version_control_system

Why should I use a Version Control System?
==========================================

Version Control Systems are a repository of your source code and allow you to
track changes inside of your project. Using a Version Control System has a few
very fortunate side effects:

Never loose code again
    One of the biggest difficulties in involving multiple developers on your
    projects is that without a VCS there is a very high chance that the developers
    will overwrite each other's changes.

You always know what's changed.
    Which means that you're never get into a situation where you don't know why
    something is not working anymore. At any point you can compare different
    version of your project to find out what's changed and what might be
    causing the problem.

You can do it again
    Ever do similar project more then once? Well, having a version control system
    allows you to create patches that you can apply to a new projet and save
    yourself a lot of time.
    
It's the right thing to do
    It allows for a better development process and workflow. Read about
    :doc:`Development Process <basics/process>`

What Version Control System are available?
==========================================

The most popular modern VCSs are `Subversion`_, `Git`_ and `Mercurial`_.

.. _Subversion: http://subversion.tigris.org/
.. _Git: http://git-scm.com/
.. _Mercurial: http://mercurial.selenic.com/
    
What is the difference between these VCSs?
==========================================

I will be brief on this subject because it's been explored by many people on
many occassions. I will include some links to additional information on this
subject.

Subversion (SVN)
    * Subversion, usually reffered to as SVN, is a centralized version control system. Which means that there is a central server that stores the repository and everyone else connects to it to download and upload code changes.
    * The central server is the only node in the system that contains all of the revision history. The SVN clients only have the `working set` and query the central server for all other information.
    * Subversion is linear, which means that if you are working on something you either have to commit everything or nothing at all. Alternatively, you can create a branch and make your changes in the branch, but branching in subversion is essentially copying, which can be slow on big projects.

Git
    * Git is a `Distributed Version Control System` (DVCS) which means that it was designed to be used by many different developers without a centralized server. The advantages over SVN is that it's FAST. It's VERY VERY FAST. But it's more complicated and takes longer to learn.
    * Unlike SVN, Git has really great branch handling. Creating, switching and working with branches is very fast.
    * Git has stash command, which gives it a huge advantage over other VSCs. stash allows to put away the changes that you're working on, so if you are in the middle of something and a client finds a bug on the site, you can fix it without impacting what you're working on.

.. _Distributed Versio Control System: http://en.wikipedia.org/wiki/Distributed_revision_control    

Mercurial
    * Mercurial is also a DVCS. It's not as fast as Git, but I hear it's easier to learn.
    * I don't use Mercurial, so, I don't have much to say about it. If someone can contribute information to this section, I would be happy to add it.

How do I setup a repository?
============================


What Version Control System should I use?
=========================================

That's a tricky question. I'm in favour of using a Distributed Version Control
System like Git or Mercurial, because they're faster then Subversion and branching
is much better on Git and Mercurial then on Subversion.


    