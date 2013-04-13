import os

ROOT = os.path.dirname(__file__)
ENV = os.getenv('ENV') or 'dev'

DEBUG=True
LOG_LEVEL='DEBUG'



PARSE_HOST='https://api.parse.com'

execfile(os.path.join(ROOT, 'config', 'secret.py'))
execfile(os.path.join(ROOT, 'config', '%s.py' % ENV))
