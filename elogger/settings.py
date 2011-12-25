import os

ROOT = os.path.dirname(__file__)
ENV = os.getenv('ENV') or 'dev'
API=''

execfile(os.path.join(ROOT, 'config', "%s.py" % ENV))