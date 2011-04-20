from __future__ import unicode_literals, print_function, division
from ConfigParser import ConfigParser
import os

ENV = os.getenv('ENV') or 'dev'
config = ConfigParser()
config.read((os.path.join(__path__[0], '%s.cfg' % ENV)))


