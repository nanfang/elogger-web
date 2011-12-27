from datetime import datetime
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
import os
from fabric.api import *
from path import path


NGINX_DIR = path('/etc/nginx/conf.d/')
DEPLOY_DIR = path('/opt/elogger')
VIRTUALENV_DIR = DEPLOY_DIR / 'python-env'
PACKAGE_DIR = DEPLOY_DIR / 'current'
PACKAGE_BACKUP_DIR = DEPLOY_DIR / 'last'
PYTHON_ENV_DIR = DEPLOY_DIR / 'python-env'

env.hosts = ['ec2-176-34-17-159.ap-northeast-1.compute.amazonaws.com']
env.user = 'elogger'

@task
def nginx():
    put('etc/nginx-elogger.conf', str(NGINX_DIR), use_sudo=True)
    sudo("/etc/init.d/nginx restart")

@task
def supervisord():
    put('etc/supervisord.conf', str(DEPLOY_DIR))

@task
def virtualenv():
    if not exists(VIRTUALENV_DIR):
        run('virtualenv --no-site-packages %s' % VIRTUALENV_DIR)

@task
def dependencies():
    virtualenv()
    put('etc/DEPENDENCIES-PROD', '%s/DEPENDENCIES' % PACKAGE_DIR)
    with prefix('. %s/bin/activate' % VIRTUALENV_DIR):
        run('pip install -r %s/DEPENDENCIES' % PACKAGE_DIR)

@task
def copy():
    with settings(warn_only=True):
        run('rm -rf %s' % PACKAGE_BACKUP_DIR)
        run('cp -r %s %s' % (PACKAGE_DIR, PACKAGE_BACKUP_DIR))
    rsync_project(PACKAGE_DIR,
                  '.',
                  exclude=(
                            '.git',
                            '.gitignore',
                           '.idea',
                           'etc',
                           '*.egg-info',
                           '*.pyc',
                           'pavement.py',
                           'deploy.sh',
                           '.DS_Store',
                           'README',
                           'fabfile.py'
                      ),
                  delete=True,
                  extra_opts='--force --chmod=g+w -O --delete-excluded')

def stop():
    with cd(DEPLOY_DIR):
        run('. %s/bin/activate && supervisorctl stop all' % PYTHON_ENV_DIR)

def start():
    virtualenv()
    with cd(DEPLOY_DIR):
        with prefix('. %s/bin/activate' % VIRTUALENV_DIR):
            run('supervisorctl stop all')
            run('supervisorctl reload')

def status():
    with cd(DEPLOY_DIR):
        run('. %s/bin/activate && supervisorctl status' % PYTHON_ENV_DIR)
