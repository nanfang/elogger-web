import os

ROOT = os.path.dirname(__file__)
ENV = os.getenv('ENV') or 'dev'

DEBUG=True
LOG_LEVEL='DEBUG'

PARSE_APPLICATION_ID='dummy'  # in secret.py
PARSE_REST_API_KEY = 'dummy'  # in secret.py
PARSE_HOST='dummy'  # in secret.py

exec(open(os.path.join(ROOT, 'config', 'secret.py')).read())
exec(open(os.path.join(ROOT, 'config', '%s.py' % ENV)).read())
