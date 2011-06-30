from datetime import datetime
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
import os

from fabric.api import *
from path import path

DEPLOY_DIR = path('/opt/elogger')
PACKAGE_DIR = DEPLOY_DIR / 'deployed'
PYTHON_ENV_DIR = DEPLOY_DIR / 'python-env'

env.hosts = ['elogger.me']

def stop_all():
    with cd(PACKAGE_DIR):
        run('. %s/bin/activate && supervisorctl stop all' % PYTHON_ENV_DIR)

def copy_files():
    rsync_project(PACKAGE_DIR, '.',
                  exclude=('.git**', '.idea**', 'build', 'api',  '*.egg-info*', 'python-env**', 'log**', '*.egg-info', '*.pyc', 'fab.py'),
                  delete=True, extra_opts='--force --chmod=g+w -O')

def install():
    with cd(PACKAGE_DIR):
        run('. %s/bin/activate && pip install -r dependencies.txt && paver develop' % PYTHON_ENV_DIR)

def start_all():
    with cd(PACKAGE_DIR):
        run('. %s/bin/activate && supervisorctl stop all' % PYTHON_ENV_DIR)
        run('. %s/bin/activate && supervisorctl reload' % PYTHON_ENV_DIR)

def status():
    with cd(PACKAGE_DIR):
        run('. %s/bin/activate && supervisorctl status' % PYTHON_ENV_DIR)

def deploy_api():
    local('~/Application/google_appengine/appcfg.py update api/')
