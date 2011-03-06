from paver.setuputils import setup
from paver.easy import *

setup(
        name="Event Logger",
        packages=['eventlogger'],
        version="0.1",
        )

@task
def build_dep(options):
    sh('pip install -q -r dependencies.txt')