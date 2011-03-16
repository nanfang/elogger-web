from paver.setuputils import setup
from paver.easy import *

setup(
        name="eLogger",
        packages=['elogger'],
        version="0.1",
        )

@task
def build_dep(options):
    sh('pip install -q -r dependencies.txt')