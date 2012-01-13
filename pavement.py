from paver.setuputils import setup
from paver.easy import *

setup(
        name="eLogger Web",
        packages=['elogger'],
        version="2.0",
        )

@task
def build_dep(options):
    sh('pip install -q -r etc/DEPENDENCIES-PROD')