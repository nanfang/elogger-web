import os

ROOT = os.path.dirname(__file__)
ENV = os.getenv('ENV') or 'dev'

DEBUG=True
API_HOST='http://localhost:8080'

execfile(os.path.join(ROOT, 'config', "%s.py" % ENV))