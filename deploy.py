from datetime import datetime
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
import os

from fabric.api import *
from path import path

DEPLOY_DIR = path('/opt/event-logger')
PACKAGE_DIR = DEPLOY_DIR / 'deployed'
PYTHON_ENV_DIR = DEPLOY_DIR / 'python-env'

env.hosts = ['ec2-174-129-160-32.compute-1.amazonaws.com']

def stop_all():
    with cd('%s/deployed' % DEPLOY_DIR):
        run('. %s/bin/activate && supervisorctl stop all' % PYTHON_ENV_DIR)

def copy_files():
    rsync_project(PACKAGE_DIR, '.',
                  exclude=('.git**', '.idea**', 'python-env**', 'log**', '*.egg-info', '*.pyc', 'fab.py'),
                  delete=True, extra_opts='--force --chmod=g+w -O')

def install():
    with cd(PACKAGE_DIR):
        run('. %s/bin/activate && pip install -r dependencies.txt && paver develop' % PYTHON_ENV_DIR)

def start_all():
    with cd(DEPLOY_DIR):
        run('. %s/bin/activate && supervisorctl -u msx -p f1reh0rse reload' % PYTHON_ENV_DIR)

def status():
    with cd(DEPLOY_DIR):
        run('. %s/bin/activate && supervisorctl -u msx -p f1reh0rse status' % PYTHON_ENV_DIR)
