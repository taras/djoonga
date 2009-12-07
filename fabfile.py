from __future__ import with_statement
from fabric.api import local, run, sudo, env, require
from fabric.context_managers import show
from fabric.contrib.project import rsync_project

def live():
	'''
	Live server configuration settings
	'''
	env.hosts = ['djoonga.com']
	env.user = 'root'
	env.path = '/var/www/djoonga.com/html/'

def build():
	'''
	Run sphinx build command on docs directory
	'''
	print local('./bin/sphinx-build -a -E docs/ docs/.build/html', capture=False)

def upload():
	'''
	Upload built files to the server
	'''
	require('path', used_for='Upload path is required. Did you forget to include live in fab parameters?')
	rsync_project(remote_dir=env.path, local_dir='docs/.build/html/')	
